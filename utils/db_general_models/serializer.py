from rest_framework import serializers
import re

from utils.db_general_models.models import UtilLang, UtilCountry, UtilCity


class LangSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lang_iso = serializers.CharField(required=True)
    lang_cn = serializers.CharField(required=True)
    lang_code639 = serializers.CharField(required=True)

    def create(self, validated_data):
        cate = UtilLang.objects.create(**validated_data)
        return cate

    def update(self, instance, validated_data):
        instance.lang_iso = validated_data['lang_iso']
        instance.lang_cn = validated_data['lang_cn']
        instance.lang_code639 = validated_data['lang_code639']
        instance.save()
        return instance


class CitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    #SlugRelatedField用于处理外键关系。它需要一个查询集（这里是从UtilCountry模型获取的所有对象），
    #SlugRelatedField使用slug_field参数指定外键字段的名称。序列化或反序列化时都可以用ID之外的其他字段来定位外键关联的对象
    #原理在于当序列化器处理请求数据时，它自动将slug_field指定的字段换为相应的UtilCountry对象。
    country = serializers.SlugRelatedField(slug_field='country_cn', queryset=UtilCountry.objects.all())

    class Meta:
        model = UtilCity
        fields = '__all__'

    def create(self, validated_data):
        cate = UtilCity.objects.create(**validated_data)
        return cate

    def update(self, instance, validated_data):
        instance.country_en = validated_data['country_en']
        instance.country_cn = validated_data['country_cn']
        instance.country = validated_data['country']
        instance.save()
        return instance


class CountrySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    country_en = serializers.CharField(required=True)
    country_cn = serializers.CharField(required=True)
    short_Len2 = serializers.CharField(required=True)
    region = serializers.CharField(required=True)

    def create(self, validated_data):
        cate = UtilCountry.objects.create(**validated_data)
        return cate

    def update(self, instance, validated_data):
        instance.country_en = validated_data['country_en']
        instance.country_cn = validated_data['country_cn']
        instance.short_Len2 = validated_data['short_Len2']
        instance.region = validated_data['region']
        instance.save()
        return instance
