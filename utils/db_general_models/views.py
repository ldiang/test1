from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from utils.db_general_models.models import UtilLang, UtilCountry, UtilCity, \
    UtilSector, UtilTheme
from utils.db_general_models.serializer import LangSerializer, \
    CountrySerializer, CitySerializer, SectorSerializer, ThemeSerializer, \
    SectorRebuildSerializer
from django.utils.translation import activate, deactivate_all
from rest_framework import status


# Create your views here.
class DB_Manage_Lang(GenericViewSet):
    queryset = UtilLang.objects.all()
    serializer_class = LangSerializer

    def create(self, request):
        data = request.data
        print(request.data)
        ser = self.get_serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response({"code": 0,
                             "message": "添加语言分类成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors)

    def list(self, request):
        lang = self.get_queryset()
        ser = self.get_serializer(lang, many=True)
        # return Response(ser.data)
        return Response({"code": 0,
                         "message": "获取语言列表成功！",
                         "data": ser.data,
                         "tableHeader": {
                             "lang_iso": "语言(英文名)",
                             "lang_cn": "语言(中文名)",
                             "lang_code639": "ISO639代码"
                         }
                         })


class DB_Manage_country(GenericViewSet):
    queryset = UtilCountry.objects.all()
    serializer_class = CountrySerializer

    def create(self, request):
        data = request.data
        print(request.data)
        ser = self.get_serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response({"code": 0,
                             "message": "添加国家成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors)

    def list(self, request):
        country = self.get_queryset()
        ser = self.get_serializer(country, many=True)
        # return Response(ser.data)
        return Response({"code": 0,
                         "message": "获取国家列表成功！",
                         "data": ser.data,
                         "total": country.count(),
                         "tableHeader": {
                             "country_en": "国家(英文)",
                             "country_cn": "国家(中文)",
                             "short_Len2": "国家代码",
                             "region": "所在洲",
                         }
                         })


class DB_Manage_city(GenericViewSet):
    queryset = UtilCity.objects.all()
    serializer_class = CitySerializer

    def create(self, request):
        data = request.data
        ser = self.get_serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response({"code": 0,
                             "message": "添加城市成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors)

    def list(self, request):
        city = self.get_queryset()
        ser = self.get_serializer(city, many=True)
        print(city)
        return Response({"code": 0,
                         "message": "获取城市列表成功！",
                         "data": ser.data,
                         "total": city.count(),
                         "tableHeader": {
                             "city_en": "城市(英文)",
                             "city_cn": "城市(中文)",
                             "country": "国家"
                         }
                         })

    def destroy(self, request):
        cityid = request.GET.get('id')
        print(cityid)
        city = UtilCity.objects.get(id=cityid)
        city.delete()
        return Response({"code": 0,
                         "message": "删除城市成功！"})


class DB_Manage_sector(GenericViewSet):
    queryset = UtilSector.objects.all()
    serializer_class = SectorSerializer

    def create(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)

        data = request.data.copy()

        if 'parent_sector' not in data:
            data['parent_sector'] = ''
        print(data)
        ser = self.get_serializer(data=data, context={'lang': lang})
        if ser.is_valid():
            activate(lang)
            ser.save()
            deactivate_all()

            return Response({"code": 0,
                             "message": "添加分类成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(
                {'code': 2, 'message': f'删除失败！原因：{ser.errors}'},
                status=status.HTTP_200_OK)

    def list(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        print(lang)

        sector_list = self.get_queryset()

        ser = self.get_serializer(sector_list, many=True,
                                  context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取产品类别成功！",
                         "data": ser.data,
                         "total": sector_list.count(),
                         "tableHeader": {
                             "sector": "产品类别",
                             "parent_sector": "父级类别",
                         }
                         })

    def destroy(self, request):
        id = request.GET.get('id')
        try:
            expo = UtilSector.objects.get(id=id)
            expo.delete()
            return Response({'code': 0, 'message': '删除成功！'},
                            status=status.HTTP_200_OK)
        except UtilSector.DoesNotExist:
            return Response({'code': 1, 'message': '您要删除的分类不存在'},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'code': 2, 'message': f'删除失败！原因：{str(e)}'},
                status=status.HTTP_200_OK)


class DB_Manage_theme(GenericViewSet):
    queryset = UtilTheme.objects.all()
    serializer_class = ThemeSerializer

    def create(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)

        data = request.data.copy()
        if 'sector' in data and not data['sector']:
            data.pop('sector', None)
        ser = self.get_serializer(data=data, context={'lang': lang})
        if ser.is_valid():
            activate(lang)
            ser.save()
            deactivate_all()

            return Response({"code": 0,
                             "message": "添加主题成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(
                {'code': 2, 'message': f'删除失败！原因：{ser.errors}'},
                status=status.HTTP_200_OK)

    def list(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)

        theme_list = self.get_queryset()

        ser = self.get_serializer(theme_list, many=True,
                                  context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取主题信息成功！",
                         "data": ser.data,
                         "total": theme_list.count(),
                         "tableHeader": {
                             "theme": "主题",
                             "sector": "产品类别",
                         }
                         })

    def destroy(self, request):
        id = request.GET.get('id')
        try:
            expo = UtilTheme.objects.get(id=id)
            expo.delete()
            return Response({'code': 0, 'message': '删除成功！'},
                            status=status.HTTP_200_OK)
        except UtilTheme.DoesNotExist:
            return Response({'code': 1, 'message': '您要删除的主题不存在'},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'code': 2, 'message': f'删除失败！原因：{str(e)}'},
                status=status.HTTP_200_OK)


class DB_Manage_sector_rebuild(GenericViewSet):
    queryset = UtilSector.objects.filter(parent_sector__isnull=True)
    serializer_class = SectorRebuildSerializer

    def list(self, request):
        lang = request.GET.get('lang', 'zh-Hans')
        activate(lang)
        print(lang)

        sector_list = self.get_queryset()

        ser = self.get_serializer(sector_list, many=True,
                                  context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取产品类别成功！",
                         "data": ser.data,
                         "total": sector_list.count(),
                         "tableHeader": {
                             "sector": "产品类别",
                             "parent_sector": "父级类别",
                         }
                         })