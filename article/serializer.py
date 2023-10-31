from rest_framework import serializers
from article.models import ArticleStore
from article.intermediate import IntermediateArticleCate
import re

from users.models import UserStore


class ArticleCateSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=False)
    cate_id = serializers.IntegerField()

    def create(self, validated_data):
        intermediate = IntermediateArticleCate.objects.create(**validated_data)
        return intermediate

    def update(self, instance, validated_data):
        # 更新数据
        instance.cate_id = validated_data['cate_id']
        instance.save()
        return instance


class ArticlesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    content = serializers.CharField(max_length=10000)
    cover_img = serializers.ImageField(required=False)
    state = serializers.CharField(required=False)
    # author_id = serializers.IntegerField()
    author_id = serializers.SlugRelatedField(slug_field='id',
                                             queryset=UserStore.objects.all())

    pub_date = serializers.DateTimeField()
    username = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    #cate_id = serializers.IntegerField(required=False)
    cate_name = serializers.CharField(required=False)
    cate_alias = serializers.CharField(required=False)

    def validate_title(self, value):
        pattern = r'^[a-zA-Z0-9\u4e00-\u9fa5？！。]{1,30}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("标题格式不合法")
        return value

    def validate_state(self, value):
        if value not in ["已发布", "草稿"]:
            raise serializers.ValidationError("状态必须是'已发布'或'草稿'")
        return value

    def create(self, validated_data):
        article = ArticleStore.objects.create(**validated_data)
        return article

    def update(self, instance, validated_data):
        # 更新数据
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.cover_img = validated_data['cover_img']
        instance.state = validated_data['state']
        instance.save()
        return instance
