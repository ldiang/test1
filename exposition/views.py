from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.db_general_models.models import UtilCountry, UtilCity
from exposition.models import ExpoStaticData
from exposition.serializer import ExpoStaticInfoListSerializer, \
    ExpoStaticInfoSerializer
from django.utils.translation import activate, deactivate_all

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
        # country = UtilCountry.objects.get(country_cn=data['country']).id
        # city = UtilCity.objects.get(city_cn=data['city']).id
        # data['country'] = country
        # data['city'] = city

        lang = request.GET.get('lang')
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
        lang = request.GET.get('lang','zh-Hans')
        activate(lang)
        print(lang)

        expo_list = ExpoStaticData.objects.all()

        ser = self.get_serializer(expo_list, many=True, context={'lang': lang})
        return Response({"code": 0,
                         "message": "获取展会基础信息成功！",
                         "data": ser.data,
                         "total": expo_list.count()})

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
