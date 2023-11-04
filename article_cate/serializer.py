from rest_framework import serializers
import re

from article_cate.models import ArticleCateStore

class CatesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    cate_name = serializers.CharField(required=True)
    cate_alias = serializers.CharField(required=True)
    #因为外键被自动添加了_id,所以这里用creator_id只参加反序列化过程
    creator_id = serializers.IntegerField(write_only=True, required=False)


    def validate_cat_name(self, value):
        if not re.match("^\S{1,10}$", value):
            raise serializers.ValidationError('1-10个非空格字符')
        return value

    def validate_cate_alias(self, value):
        if not re.match("^[a-zA-Z0-9]{1,15}$", value):
            raise serializers.ValidationError('1-15个大小写字母和数字组成的字符串')
        return value

    def create(self, validated_data):
        cate = ArticleCateStore.objects.create(**validated_data)
        return cate

    def update(self, instance, validated_data):
        instance.cate_name = validated_data['cate_name']
        instance.cate_alias = validated_data['cate_alias']
        instance.save()
        return instance