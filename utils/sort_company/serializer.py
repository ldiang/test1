from rest_framework import serializers
from modeltranslation.utils import build_localized_fieldname
from django.utils.translation import activate, deactivate_all

from utils.db_general_models.models import UtilCountry
from utils.sort_company.models import SortCompanyStore, \
    IntermediateCompanySector, IntermediateCompanyTheme


class SortCompaniesActionSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field='country_cn',
        queryset=UtilCountry.objects.all())

    class Meta:
        model = SortCompanyStore
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        lang = self.context.get('lang', 'en')
        activate(lang)
        lang_codes = ['zh-Hans', 'de']

        for lang_index in lang_codes:
            description_field = build_localized_fieldname('description',
                                                          lang_index)
            if getattr(instance, description_field) is not None:
                break  # 如果找到非空的描述字段，退出循环
        else:
            description_field = build_localized_fieldname('description', 'en')

        city_name = instance.city.city_cn if instance.city and instance.city.city_cn else instance.city.city_en

        data = {
            'id': instance.id,
            'name': instance.name,
            'country': representation.get('country'),
            'city': city_name,
            'website': instance.website,
            'description': instance.description,
            'established': instance.established,
            'num_staff': instance.num_staff,
            'sector': representation.get('sector'),
            'theme': representation.get('theme'),
        }

        return data

    def create(self, validated_data):
        company = SortCompanyStore.objects.create(**validated_data)
        return company

    def update(self, instance, validated_data):
        instance.city = validated_data['city']
        instance.website = validated_data['website']
        instance.description = validated_data['description']
        instance.established = validated_data['established']
        instance.num_staff = validated_data['num_staff']
        instance.save()
        return instance


class IntermediateCompanySectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateCompanySector
        fields = '__all__'

    def create(self, validated_data):
        intermediate = IntermediateCompanySector.objects.create(
            **validated_data)
        return intermediate


class IntermediateCompanyThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateCompanyTheme
        fields = '__all__'

    def create(self, validated_data):
        intermediate = IntermediateCompanyTheme.objects.create(**validated_data)
        return intermediate
