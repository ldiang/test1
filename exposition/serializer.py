from modeltranslation.utils import build_localized_fieldname
from rest_framework import serializers

from utils.db_general_models.models import UtilCountry, UtilCity
from exposition.models import ExpoStaticData
from django.utils.translation import activate, deactivate_all


class ExpoStaticInfoListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    country = serializers.SlugRelatedField(
        slug_field='country_cn',
        queryset=UtilCountry.objects.all())
    city = serializers.SlugRelatedField(
        slug_field='city_cn',
        queryset=UtilCity.objects.all())
    rating = serializers.IntegerField(required=True)
    website = serializers.URLField(required=True)

    class Meta:
        model = ExpoStaticData
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        lang = self.context.get('lang', 'en')
        name_field = build_localized_fieldname('name', lang)
        data = {
            'id': instance.id,
            'name': getattr(instance, name_field),
            'country': representation.get('country'),
            'city': representation.get('city'),
            'rating': instance.rating,
            'website': instance.website,
        }

        return data

    def create(self, validated_data):
        # activate('zh-Hans')
        expo_static_info = ExpoStaticData.objects.create(**validated_data)
        # deactivate_all()
        # expostaticinfo = ExpoStaticData.objects.populate(False).create(**validated_data)
        return expo_static_info


class ExpoStaticInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    country = serializers.SlugRelatedField(
        slug_field='country_cn',
        queryset=UtilCountry.objects.all())
    city = serializers.SlugRelatedField(
        slug_field='city_cn',
        queryset=UtilCity.objects.all())
    rating = serializers.IntegerField(required=True)
    website = serializers.URLField(required=True)

    class Meta:
        model = ExpoStaticData
        # fields = '__all__'
        fields = ('name', 'country', 'city', 'rating', 'website')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 获取前端请求的语言
        lang = self.context.get('lang', 'en')

        # 获取需要返回的字段名
        name_field = build_localized_fieldname('name', lang)

        # 构建返回的数据
        data = {
            'id': instance.id,
            'name': getattr(instance, name_field),
            'country': representation.get('country'),
            'city': representation.get('city'),
            'rating': instance.rating,
            'website': instance.website
        }

        return data
