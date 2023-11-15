from modeltranslation.utils import build_localized_fieldname
from rest_framework import serializers

from utils.db_general_models.models import UtilCountry, UtilCity, UtilSector, \
    UtilTheme
from exposition.models import ExpoStaticData, ExpoStore, IntermediateExpoSector, \
    IntermediateExpoTheme
from django.utils.translation import activate, deactivate_all
import logging


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
    short_len2 = serializers.CharField(source='country.short_Len2',
                                       read_only=True)  # 新增这一行

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
            'countrycode': representation.get('short_len2')
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


class IntermediateExpoSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateExpoSector
        fields = '__all__'

    def create(self, validated_data):
        intermediate = IntermediateExpoSector.objects.create(**validated_data)
        return intermediate


class IntermediateExpoThemeSerializer(serializers.ModelSerializer):
    theme = serializers.PrimaryKeyRelatedField(queryset=UtilTheme.objects.all())

    sector = serializers.PrimaryKeyRelatedField(
        queryset=UtilSector.objects.all(), required=False)

    class Meta:
        model = IntermediateExpoSector
        fields = '__all__'

    def create(self, validated_data):
        intermediate = IntermediateExpoTheme.objects.create(**validated_data)
        return intermediate


class ExpoAnnualInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoStore
        fields = '__all__'

    def create(self, validated_data):
        expo_store = ExpoStore.objects.create(**validated_data)
        return expo_store


class ExpoAnnualInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoStore
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 获取前端请求的语言
        lang = self.context.get('lang', 'zh-Hans')

        # 获取需要返回的字段名
        name_field = build_localized_fieldname('description', lang)
        print("name_field:", name_field)
        print("instance:", instance)
        # 构建返回的数据
        # 注意外键需要用representation.get('name')
        data = {
            'id': representation.get('name'),
            'annual_id': instance.id,
            'description': getattr(instance, name_field),
            'date': instance.date,
            'num_expos': instance.num_expos,
            'num_visit': instance.num_visit,
            'sector': representation.get('sector'),
            'theme': representation.get('theme')
        }
        return data
