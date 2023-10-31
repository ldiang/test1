from django.core.validators import EmailValidator
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
        model = UserStore
        # fields = '__all__'
        fields = ('id', 'username', 'password', 'repassword', 'is_staff')

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
        user = UserStore.objects.create_user(username=username,
                                             password=password)

        return user


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    nickname = serializers.CharField()
    email = serializers.EmailField(validators=[EmailValidator(
        message='Invalid email format')])
    user_pic = serializers.CharField(max_length=2000)

    class Meta:
        model = UserStore
        fields = ('id', 'username', 'nickname', 'email', 'user_pic')

    def validate_nickname(self, value):
        if not (1 <= len(value) <= 10):
            raise serializers.ValidationError('用户名长度必须在1到10位之间')
        if not re.match("^[a-zA-Z0-9]*$", value):
            raise serializers.ValidationError('用户名只能包含大小写字母和数字')
        return value

    def update(self, instance, validated_data):
        # 更新数据
        instance.nickname = validated_data['nickname']
        instance.email = validated_data['email']
        instance.user_pic = validated_data['user_pic']
        instance.save()
        return instance

class UserPasswordResetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    new_pwd = serializers.CharField(write_only=True, required=False)
    re_pwd = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserStore
        fields = ('id', 'username', 'password', 'new_pwd', 're_pwd')

    def validate(self, value):
        new_pwd = value['new_pwd']
        re_pwd = value['re_pwd']

        if len(re_pwd) < 6 or len(re_pwd) > 15:
            raise serializers.ValidationError('密码长度必须在6到15位之间')
        if ' ' in re_pwd:
            raise serializers.ValidationError('密码不能包含空格')
        if len(new_pwd) < 6 or len(new_pwd) > 15:
            raise serializers.ValidationError('密码长度必须在6到15位之间')
        if ' ' in new_pwd:
            raise serializers.ValidationError('密码不能包含空格')
        if re_pwd != new_pwd:
            raise serializers.ValidationError('输入的两次新密码不相同')

        return value

    def update(self,instance, validated_data):
        # 更新数据
        instance.set_password(validated_data['new_pwd'])

        instance.save()
        return instance

class GroupSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(required=False)