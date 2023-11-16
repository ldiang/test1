from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.db_general_models.models import UtilCountry, UtilCity, UtilSector, \
    UtilTheme
from exposition.models import ExpoStaticData, ExpoStore, IntermediateExpoSector, \
    IntermediateExpoTheme
from exposition.serializer import ExpoStaticInfoListSerializer, \
    ExpoStaticInfoSerializer, ExpoAnnualInfosSerializer, \
    IntermediateExpoSectorSerializer, IntermediateExpoThemeSerializer, \
    ExpoAnnualInfoSerializer
from django.utils.translation import activate, deactivate_all
from datetime import datetime

from django.utils import translation
from modeltranslation.translator import translator
from modeltranslation.utils import get_language, get_translation_fields


# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ExpoStaticInfoList(GenericViewSet):
    queryset = ExpoStaticData.objects.all()
    serializer_class = ExpoStaticInfoListSerializer

    def create(self, request):
        data = request.data.copy()
        print(data)
        # country = UtilCountry.objects.get(country_cn=data['country']).id
        # city = UtilCity.objects.get(city_cn=data['city']).id
        # data['country'] = country
        # data['city'] = city

        lang = request.GET.get('lang', 'zh-Hans')
        print(lang)
        ser = self.get_serializer(data=data, context={'lang': lang})
        if ser.is_valid():

            # translator.cache = {}  # 清除缓存
            activate(lang)
            # deactivate_all()
            ser.save()
            deactivate_all()

            return Response({"code": 0,
                             "message": "添加展会基础信息成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        print(lang)

        expo_list = ExpoStaticData.objects.all()

        ser = self.get_serializer(expo_list, many=True, context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取展会基础信息成功！",
                         "data": ser.data,
                         "total": expo_list.count(),
                         "tableHeader": {
                             "name": "展会名称",
                             "country": "国家",
                             "city": "城市",
                             "rating": "评分",
                             "website": "官网",
                             "countrycode": "国家代码",
                         }
                         })

    def destroy(self, request):
        id = request.GET.get('id')
        try:
            expo = ExpoStaticData.objects.get(id=id)
        except ExpoStaticData.DoesNotExist:
            return Response({'code': 1, 'message': '您要删除的展会不存在'},
                            status=status.HTTP_200_OK)

        expo.delete()
        return Response({'code': 0, 'message': '删除成功！'},
                        status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ExpoStaticInfo(GenericViewSet):
    queryset = ExpoStaticData.objects.all()
    serializer_class = ExpoStaticInfoSerializer

    def retrieve(self, request):
        id = request.GET.get('id')

        lang = request.GET.get('lang', 'zh-Hans')

        activate(lang)
        expo = ExpoStaticData.objects.get(id=id)
        print(id)

        ser = self.get_serializer(expo, context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取展会基础信息成功！",
                         "data": ser.data})

    def update(self, request):
        data = request.data.copy()
        id = request.GET.get('id')
        expo = ExpoStaticData.objects.get(id=id)

        # 从前端读取需要更新的语言
        lang = request.GET.get('lang')

        # 通过键值对遍历，自动生成需更新的字段名称
        # key 是 name, value是慕尼黑汽车展德语
        for key, value in data.items():
            if value:
                translation_field = f'{key}_{lang}'
                # 检查字段是否存在
                if hasattr(expo, translation_field):
                    # 根据前端信息修改指定内容
                    setattr(expo, translation_field, value)

        expo.save()

        # 返回更新后的数据
        ser = ExpoStaticInfoSerializer(expo, context={'lang': lang})
        return Response({"code": 0,
                         "message": "修改展会基础信息成功！",
                         "data": ser.data})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ExpoAnnualInfos(GenericViewSet):
    queryset = ExpoStore.objects.all()
    serializer_class = ExpoAnnualInfosSerializer

    def create(self, request):
        data = request.data.copy()
        print(data)
        data['name'] = ExpoStaticData.objects.get(id=data['name']).id
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        data['year'] = int(data['year'])

        data['num_expos'] = int(data['num_expos'])
        data['num_visit'] = int(data['num_visit'])

        # 第1步：将data['sector']和data['theme']从data中提取出来
        sectors_data = data.pop('sector', [])
        themes_data = data.pop('theme', [])

        # 第2步：用list(map(int, sectors_data.split(',')))将data['sector']和data['theme']转为真正的数组
        sector_ids = list(map(int, sectors_data[0].split(',')))
        theme_ids = list(map(int, themes_data[0].split(',')))

        # 第3步：利用数组对UtilSector和UtilTheme进行查询，组成由对象组成的新的data['sector']和data['theme']
        sector_instances = UtilSector.objects.filter(id__in=sector_ids)
        theme_instances = UtilTheme.objects.filter(id__in=theme_ids)

        # 第4步：将新的data['sector']和data['theme']更新到data中然后传入序列化器
        data['sector'] = sector_instances
        data['theme'] = theme_instances

        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        # 第5步：主数据写入数据库
        ser = self.get_serializer(data=data, context={'lang': lang})
        if ser.is_valid():

            activate(lang)
            # deactivate_all()
            ser.save()
            deactivate_all()
            # 第6步：构建新的中间表实例，先找刚保存的主数据的对象
            new_expoAnnualInfo = ExpoStore.objects.get(id=ser.instance.id)
            print(new_expoAnnualInfo)
            # 第7步：根据之前获取的分类对象列表构建新实例，并进行验证
            for sector in sector_instances:

                new_intermediate = [
                    {'expo': new_expoAnnualInfo.id, 'sector': sector.id}]
                new_res = IntermediateExpoSectorSerializer(
                    data=new_intermediate, many=True)

                if new_res.is_valid():
                    new_res.save()
                else:
                    print(new_res.errors)
            # 第8步：另外一个中间表同样的操作方式
            for theme in theme_instances:
                new_intermediate = [
                    {'expo': new_expoAnnualInfo.id, 'theme': theme.id}]
                print(new_intermediate)
                new_res = IntermediateExpoThemeSerializer(
                    data=new_intermediate, many=True)

                if new_res.is_valid():
                    new_res.save()
                else:
                    print(new_res.errors)

            return Response({"code": 0,
                             "message": "添加展会年度信息成功！",
                             "data": ser.data})

        else:
            print(ser.errors)

            return Response({"code": 1,
                             "message": "添加展会年度信息失败！",
                             "data": ser.errors})


class ExpoAnnualInfo(GenericViewSet):
    queryset = ExpoStore.objects.all()
    serializer_class = ExpoAnnualInfoSerializer

    def retrieve(self, request):
        id = request.GET.get('id')
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        expo_instance = ExpoStaticData.objects.get(id=id).id
        if ExpoStore.objects.filter(
                name=expo_instance).order_by('-year').first():
            # 现在latest_expo_info就是具有最大year值的对象
            latest_expo_annual_info = ExpoStore.objects.filter(
                name=expo_instance).order_by('-year').first()

            ser = ExpoAnnualInfoSerializer(latest_expo_annual_info, context={'lang': lang})
            deactivate_all()
            return Response({"code": 0,
                                 "message": "获取展会年度信息成功！",
                                 "data": ser.data})
        else:
            deactivate_all()
            return Response({"code": 1,
                             "message": "该展会尚未建立年度信息报告"})


