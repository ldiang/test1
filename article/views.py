from datetime import datetime

from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from article.models import ArticleStore
from article.serializer import ArticlesSerializer
from users.models import UserStore
import os


# Create your views here.
class Articles(GenericViewSet):
    queryset = ArticleStore.objects.all()
    serializer_class = ArticlesSerializer

    def list(self, request):
        books = self.get_queryset()
        ser = self.get_serializer(books, many=True)
        return Response(ser.data)

    def create(self, request):
        data = request.data
        username = request.user.username
        user = UserStore.objects.get(username=username)
        author_id = user.id
        pub_date = datetime.now()
        data['author_id'] = author_id
        data['pub_date'] = pub_date

        ser = self.get_serializer(data=data)
        ser.is_valid()
        ser.save()

        # 注意 前端传来表格数据中cover_img是file类型 包含文件本地地址
        # cover_img_file这就是前端传来的文件对象
        cover_img_file = request.FILES.get('cover_img')
        if cover_img_file:
            # 生成封面图片保存的路径，存储在STATIC_URL目录下
            filename = os.path.join('img', cover_img_file.name)
            ser.cover_img.save(filename, ContentFile(cover_img_file.read()),
                               save=True)
        return Response(ser.data)
