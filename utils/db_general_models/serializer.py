from rest_framework import serializers
from modeltranslation.utils import build_localized_fieldname

from utils.db_general_models.models import UtilLang, UtilCountry, UtilCity, \
    UtilSector, UtilTheme


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

    # SlugRelatedField用于处理外键关系。它需要一个查询集（这里是从UtilCountry模型获取的所有对象），
    # SlugRelatedField使用slug_field参数指定外键字段的名称。序列化或反序列化时都可以用ID之外的其他字段来定位外键关联的对象
    # 原理在于当序列化器处理请求数据时，它自动将slug_field指定的字段换为相应的UtilCountry对象。


class CitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    city_en = serializers.CharField(required=False)
    city_cn = serializers.CharField(required=False)
    country = serializers.SlugRelatedField(slug_field='country_cn',
                                           queryset=UtilCountry.objects.all(),required=False)

    class Meta:
        model = UtilCity
        fields = '__all__'

    def create(self, validated_data):
        city = UtilCity.objects.create(**validated_data)
        return city

    def update(self, instance, validated_data):
        # 检查 'city_en' 是否在 validated_data 中，并且不为 None
        if 'city_en' in validated_data and validated_data['city_en'] is not None:
            instance.city_en = validated_data['city_en']

        if 'city_cn' in validated_data and validated_data['city_cn'] is not None:
            instance.city_cn = validated_data['city_cn']

        if 'country' in validated_data and validated_data['country'] is not None:
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


class SectorSerializer(serializers.ModelSerializer):
    parent_sector = serializers.SlugRelatedField(slug_field='sector',
                                                 queryset=UtilSector.objects.all(),
                                                 required=False,
                                                 allow_null=True)

    class Meta:
        model = UtilSector
        fields = ('id', 'sector', 'parent_sector')

    def create(self, validated_data):
        sector = UtilSector.objects.create(**validated_data)
        return sector


class ThemeSerializer(serializers.ModelSerializer):
    sector = serializers.SlugRelatedField(slug_field='sector',
                                          queryset=UtilSector.objects.all())

    class Meta:
        model = UtilTheme
        fields = ('id', 'theme', 'sector')

    def create(self, validated_data):
        sector = UtilTheme.objects.create(**validated_data)
        return sector


class SectorRebuildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = UtilSector
        fields = ('id', 'sector', 'parent_sector', 'children')

    def get_children(self, obj):
        children = UtilSector.objects.filter(parent_sector=obj)
        return SectorRebuildSerializer(children, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        lang = self.context.get('lang', 'zh-Hans')
        sector_field = build_localized_fieldname('sector', lang)
        sector_value = instance.__dict__.get(sector_field, None)

        data = {
            'id': instance.id,
            'value': sector_value,
            'label': sector_value,
            'children': self.get_children(instance)
        }

        if not instance.parent_sector:  # Check if parent_sector is None
            data['value'] = sector_value
            data['label'] = sector_value
            data.pop('sector', None)
            data.pop('parent_sector', None)

        if not data['children']:
            data.pop('children', None)

        return data
