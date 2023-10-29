from rest_framework import serializers
from users.models import UserStore
import re


class UserStoreSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    repassword = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(default=True, write_only=True)

    class Meta:
        model=UserStore
        #fields = '__all__'
        fields=('id','username','password', 'repassword', 'is_staff')

    def validate(self, value):
        password = value['password']
        repassword = value['repassword']

        if len(password) < 6 or len(repassword) > 15:
            raise serializers.ValidationError('密码长度必须在6到15位之间')
        if ' ' in password:
            raise serializers.ValidationError('密码不能包含空格')
        if password != repassword:
            raise serializers.ValidationError('两次密码输入不相同')
        return value

    def validate_username(self, value):
        if not (1 <= len(value) <= 10):
            raise serializers.ValidationError('用户名长度必须在1到10位之间')
        if not re.match("^[a-zA-Z0-9]*$", value):
            raise serializers.ValidationError('用户名只能包含大小写字母和数字')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = UserStore.objects.create_user(username=username, password=password)

        return user