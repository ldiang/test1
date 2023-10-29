from rest_framework import serializers
from books.models import BookInfo

class HerosSerializer(serializers.Serializer):
    hname =serializers.CharField(max_length=20)
    hcomment = serializers.CharField(max_length=200)
class BooksSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    btitle = serializers.CharField(max_length=20, min_length=5, )
    bread = serializers.IntegerField(max_value=100, min_value=5)
    bpub_date = serializers.DateField()
    bcomment = serializers.IntegerField(default=10)
    #三种嵌套式返回 (就是把和图书相关的英雄信息一同返回)
    #heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    #heroinfo_set = serializers.StringRelatedField(read_only=True, many=True)
    #heroinfo_set = HerosSerializer(many=True)       #英雄序列化器必须放到图书序列化器之前，否则无法解析
                                                    #也就是说嵌套序列化器，内部的序列化器必须放在外部的序列化器的前面，否则会报错

    # 单一字段验证
    def validate_btitle(self, value):

        if value == 'python':
            raise serializers.ValidationError('书名不能是python')
        return value

    # 多个字段验证
    def validate(self, attrs):

        if attrs['bread'] < attrs['bcomment']:
            raise serializers.ValidationError('阅读量大于评论量')

        return attrs

    def create(self, validated_data):
        # 保存数据
        book = BookInfo.objects.create(**validated_data)

        return book

    def update(self, instance, validated_data):
        # 更新数据
        instance.btitle = validated_data['btitle']
        instance.bread = validated_data['bread']
        instance.bpub_date = validated_data['bpub_date']
        instance.bcomment = validated_data['bcomment']
        instance.save()
        return instance