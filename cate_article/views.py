from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cate_article.models import CateStore
from users.models import UserStore
from rest_framework import status


from cate_article.serializer import CatesSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Cates(GenericViewSet):
    queryset = CateStore.objects.all()
    serializer_class = CatesSerializer

    def create(self, request):
        data = request.data
        username = request.user.username
        user = UserStore.objects.get(username=username)
        data['creator_id'] = user.id
        ser = self.get_serializer(data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def list(self, request):
        cates = self.get_queryset()
        ser = self.get_serializer(cates, many=True)
        return Response(ser.data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Cate(GenericViewSet):
    def retrieve(self,request):
        id = request.GET.get('id')
        cate=CateStore.objects.get(id=id)
        ser=CatesSerializer(cate)
        return Response(ser.data)

    def update(self,request):
        id = request.GET.get('id')
        data = request.data
        cate = CateStore.objects.get(id=id)
        ser = CatesSerializer(cate, data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def destroy(self, request):
        id = request.GET.get('id')
        cate = CateStore.objects.get(id=id)
        cate.delete()
        return Response({})