from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from utils.db_general_models.models import UtilCity, UtilCountry, UtilSector, \
    UtilTheme
from utils.sort_company.models import SortCompanyStore
from utils.sort_company.serializer import SortCompaniesActionSerializer, \
    IntermediateCompanySectorSerializer, IntermediateCompanyThemeSerializer
from utils.utils_service import CityService
from django.utils.translation import activate, deactivate_all

from utils.utils_intermediate import IntermediateService


# Create your views here.
class SortCompanyAction(GenericViewSet):
    queryset = SortCompanyStore.objects.all()
    serializer_class = SortCompaniesActionSerializer

    def create(self, request):
        data = request.data
        lang = 'de'
        print(request.data)
        country = None
        if 'country' in data:
            country_name = data['country']

            if UtilCountry.objects.filter(country_cn=country_name).exists():
                country = UtilCountry.objects.get(country_cn=country_name)
            elif UtilCountry.objects.filter(country_en=country_name).exists():
                country = UtilCountry.objects.get(country_en=country_name)
            else:
                country = UtilCountry.objects.get(id=1)

        # country = UtilCountry.objects.get(country_cn=data['country'])

        try:
            city = UtilCity.objects.get(city_en=data['city'])
        except UtilCity.DoesNotExist:
            city_service = CityService()
            city = city_service.create_new_city(data['city'],
                                                country.country_cn)

        data['country'] = country.country_cn
        data['city'] = city.id

        ser = self.get_serializer(data=data)
        if ser.is_valid():
            activate(lang)
            ser.save()
            deactivate_all()

            ser_instance = ser
            field_master = 'company'
            field_detail = 'sector'
            IntermediateService.intermediate_table_save(
                data,
                SortCompanyStore,
                UtilSector,
                field_master,
                field_detail,
                ser_instance,
                IntermediateCompanySectorSerializer
            )
            field_detail = 'theme'
            IntermediateService.intermediate_table_save(
                data,
                SortCompanyStore,
                UtilTheme,
                field_master,
                field_detail,
                ser_instance,
                IntermediateCompanyThemeSerializer
            )

            return Response({"code": 0,
                             "message": "添加公司信息成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response({"code": 1,
                             "message": "添加公司信息失败！",
                             "data": ser.errors})

    def retrieve(self, request):

        id = request.GET.get('id')
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)

        try:
            company = SortCompanyStore.objects.get(id=id)
            ser = self.get_serializer(company, context={'lang': lang})
            deactivate_all()
            return Response({"code": 0, "message": "获取公司详情信息成功！",
                             "data": ser.data})

        # DoesNotExist是一个异常类，用于在查询数据库时指示对象不存在的异常。
        # 写法为 被查询的数据库名.DoesNotExist
        except SortCompanyStore.DoesNotExist:
            deactivate_all()
            return Response(
                {"code": 1, "message": "您所查询的公司信息不存在，请联系我们！"})

    def update(self, request):
        id = request.GET.get('id')
        data = request.data.copy()
        # 这次前端要发送明确的语言说明
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        company = SortCompanyStore.objects.get(id=id)

        country = UtilCountry.objects.get(country_cn=data['country'])

        city = None
        if lang == 'zh-Hans':
            if not UtilCity.objects.filter(city_cn=data['city']).exists():
                city_id = company.city.id
                city_service = CityService()
                city_ser = city_service.update_city_name_cn(city_id,
                                                            data['city'])
                if city_ser:
                    city = city_ser.instance
            else:
                city = UtilCity.objects.get(city_cn=data['city'])
        else:
            city = UtilCity.objects.get(city_en=data['city'])

        data['country'] = country
        data['city'] = city.id
        data['established'] = int(data['established'])
        data['num_staff'] = int(data['num_staff'])
        print(data)
        ser = self.get_serializer(company, data=data)

        if ser.is_valid():
            ser.save()
            ser_instance = ser
            field_master = 'company'
            field_detail = 'sector'
            IntermediateService.intermediate_table_save(
                data,
                SortCompanyStore,
                UtilSector,
                field_master,
                field_detail,
                ser_instance,
                IntermediateCompanySectorSerializer
            )
            field_detail = 'theme'
            IntermediateService.intermediate_table_save(
                data,
                SortCompanyStore,
                UtilTheme,
                field_master,
                field_detail,
                ser_instance,
                IntermediateCompanyThemeSerializer
            )

            return Response({"code": 0,
                             "message": "修改公司详情成功！",
                             "data": ser.data})

        else:
            print(ser.errors)
            return Response({"code": 1,
                             "message": "编辑公司详情失败，请修正输入内容"})

    def destroy(self, request):
        id = request.GET.get('id')
        city = SortCompanyStore.objects.get(id=id)
        city.delete()
        return Response({"code": 0,
                         "message": "删除城市成功！"})


class SortCompaniesAction(GenericViewSet):
    queryset = SortCompanyStore.objects.all()
    serializer_class = SortCompaniesActionSerializer

    def create(self, request):
        datalist = request.data
        print(datalist)
        data_num = len(datalist)

        failed_writes = 0  # 记录重复写入的次数
        failed_list = []

        try:
            for index, data in enumerate(datalist):
                try:
                    lang = 'de'
                    print(data)
                    country = None

                    if 'country' in data:
                        country_name = data['country']

                        if UtilCountry.objects.filter(
                                country_cn=country_name).exists():
                            country = UtilCountry.objects.get(
                                country_cn=country_name)
                        elif UtilCountry.objects.filter(
                                country_en=country_name).exists():
                            country = UtilCountry.objects.get(
                                country_en=country_name)
                        else:
                            country = UtilCountry.objects.get(id=1)

                    # country = UtilCountry.objects.get(country_cn=data['country'])

                    try:
                        city = UtilCity.objects.get(city_en=data['city'])
                    except UtilCity.DoesNotExist:
                        city_service = CityService()
                        city = city_service.create_new_city(data['city'],
                                                            country.country_cn)

                    data['country'] = country.country_cn
                    data['city'] = city.id

                    ser = self.get_serializer(data=data)
                    if ser.is_valid():
                        activate(lang)
                        ser.save()
                        deactivate_all()

                        ser_instance = ser
                        field_master = 'company'
                        field_detail = 'sector'
                        IntermediateService.intermediate_table_save(
                            data,
                            SortCompanyStore,
                            UtilSector,
                            field_master,
                            field_detail,
                            ser_instance,
                            IntermediateCompanySectorSerializer
                        )
                        field_detail = 'theme'
                        IntermediateService.intermediate_table_save(
                            data,
                            SortCompanyStore,
                            UtilTheme,
                            field_master,
                            field_detail,
                            ser_instance,
                            IntermediateCompanyThemeSerializer
                        )

                except IntegrityError:
                    failed_writes += 1
                    failed_list.append(data['name'])

        except Exception as e:
            # 如果在循环中发生异常，这里会捕获异常并进行处理
            return Response({"code": 1, "message": f"发生错误：{str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if failed_writes == 0:
            return Response({"code": 0,
                             "message": f"成功添加{data_num}家公司信息！"})
        else:
            return Response({"code": 1,
                             "message": f"成功添加{data_num - failed_writes}家公司信息！"
                                        f"{failed_writes}家信息重复未被写入！",
                             "data": failed_list})

    def list(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)

        company_list = SortCompanyStore.objects.all()

        ser = self.get_serializer(company_list, many=True,
                                  context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取展会基础信息成功！",
                         "data": ser.data,
                         "total": company_list.count(),
                         "tableHeader": {
                             "name": "展会名称",
                             "country": "国家",
                             "city": "城市",
                             "website": "官网",
                             "description": "企业介绍",
                             "established": "成立时间",
                             "num_staff": "员工数量",
                             "sector": "行业分类",
                             "theme": "优势方向"

                         }
                         })
