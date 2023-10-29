from rest_framework import serializers
import re

from cate_article.models import CateStore

class CatesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    cate_name = serializers.CharField(required=True)
    cate_alias = serializers.CharField(required=True)

    def validate_cat_name(self, value):
        if not re.match("^\S{1,10}$", value):
            raise serializers.ValidationError('1-10个非空格字符')
        return value

    def validate_cate_alias(self, value):
        if not re.match("^[a-zA-Z0-9]{1,15}$", value):
            raise serializers.ValidationError('1-15个大小写字母和数字组成的字符串')
        return value

    def create(self, validated_data):
        cate = CateStore.objects.create(**validated_data)
        return cate
