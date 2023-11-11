from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from utils.db_general_models.models import UtilLang, UtilCountry, UtilCity
from utils.db_general_models.serializer import LangSerializer, \
    CountrySerializer, CitySerializer


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