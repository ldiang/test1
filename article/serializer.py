from rest_framework import serializers
from article.models import ArticleStore
import re

class ArticlesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    content = serializers.CharField(max_length=10000)
    cover_img = serializers.ImageField(required=False)
    state = serializers.CharField(required=False)
    cate_id = serializers.CharField()
    author_id = serializers.CharField()
    pub_date = serializers.CharField()

    def validate_title(self,value):
        pattern = r'^[a-zA-Z0-9\u4e00-\u9fa5？！。]{1,30}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("标题格式不合法")
        return value

    def validate_state(self,value):
        if value not in ["已发布", "草稿"]:
            raise serializers.ValidationError("状态必须是'已发布'或'草稿'")
        return value

    def create(self, validated_data):
        article = ArticleStore.objects.create(**validated_data)
        return article

