from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import UserStore
from users.serializer import UserStoreSerializer, UserInfoSerializer, \
    UserPasswordResetSerializer


# Create your views here.
class UserCreate(ViewSet):
    def create(self, request):
        print(request.data)
        data = request.data
        username = data['username']
        if UserStore.objects.filter(username=username).exists():
            return Response({'message': '该用户名已存在'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = UserStoreSerializer(data=data)
        if ser.is_valid():
            ser.save()
            response = Response(ser.data)
            return response
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(ViewSet):

    def create(self, request):
        data = request.data
        received_username = data['username']
        if UserStore.objects.filter(username=received_username).exists():
            user = UserStore.objects.get(username=received_username)
            received_password = data['password']
            hashed_password = user.password
            print(hashed_password)
            passwords_match = check_password(received_password, hashed_password)
            if passwords_match:
                # return Response('您将要登录了')

                # 返回中加入token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # 将令牌转换为字典以进行序列化
                token_data = {
                    'access_token': access_token,
                    # 'refresh_token': refresh_token,
                }
                return Response(token_data, status=status.HTTP_200_OK)
            else:
                return Response('您输入的密码不正确')
        else:
            return Response('您输入的用户名不存在')


#@authentication_classes([JWTAuthentication])
#@permission_classes([IsAuthenticated])
class UserList(ViewSet):
    def list(self, request):
        users = UserStore.objects.all()
        ser = UserStoreSerializer(users, many=True)
        return Response(ser.data)

#@authentication_classes([JWTAuthentication])
#@permission_classes([IsAuthenticated])
class UserInfo(ViewSet):
    def retrieve(self,request):
        username = request.user.username
        user = UserStore.objects.get(username=username)
        ser = UserInfoSerializer(user)
        return Response(ser.data)

    def update(self,request):
        data = request.data
        username = request.user.username
        user = UserStore.objects.get(username=username)
        ser = UserInfoSerializer(user, data=data)
        #ser.is_valid()
        #ser.save()
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(ser.data)


#@authentication_classes([JWTAuthentication])
#@permission_classes([IsAuthenticated])
class UserPasswordReset(ViewSet):

    def update(self,request):
        data = request.data
        username = request.user.username
        user = UserStore.objects.get(username=username)
        if user.check_password(data['old_pwd']):
            ser = UserPasswordResetSerializer(user, data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                print(ser.errors)
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('当前密码不正确')