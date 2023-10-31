import uuid
from datetime import datetime
from django.conf.global_settings import MEDIA_ROOT

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response

from users.models import UserStore
from cate_article.models import CateStore
from article.models import ArticleStore
from article.intermediate import IntermediateArticleCate
from article.serializer import ArticlesSerializer, ArticleCateSerializer
from cincode_backend.settings import MEDIA_DIRS

import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings


# Create your views here.
class ArticlesPaginator(PageNumberPagination):
    page_size = 4
    max_page_size = 6
    page_query_param = 'pagenum'
    page_size_query_param = 'pagesize'

class Articles(GenericViewSet):
    queryset = ArticleStore.objects.all()
    serializer_class = ArticlesSerializer
    pagination_class = ArticlesPaginator

    def create(self, request):
        data = request.data.copy()  # 创建副本 尝试改写

        username = request.user.username
        user = UserStore.objects.get(username=username)

        pub_date = datetime.now()

        data['author_id'] = user.id
        data['pub_date'] = pub_date
        ser = self.get_serializer(data=data)

        if ser.is_valid():
            ser.save()
            ##############################################
            #中间表
            #ser.instance 是序列化器保存数据后返回的模型实例。
            #通过 id 过滤出唯一的 ArticleStore 对象
            new_article = ArticleStore.objects.get(title=data['title'],
                                                   id=ser.instance.id)
            new_intermediate = {'article_id': new_article.id,
                                'cate_id': data['cate_id']}
            new_res = ArticleCateSerializer(data=new_intermediate)
            if new_res.is_valid():
                new_res.save()
            ##############################################
            # 注意 前端传来表格数据中cover_img是file类型 包含文件本地地址
            # cover_img_file这就是前端传来的文件对象
            cover_img_file = request.FILES.get('cover_img')
            if cover_img_file:
                path = os.path.join(MEDIA_ROOT, 'img', cover_img_file.name)
                default_storage.save(path, ContentFile(cover_img_file.read()))

            return Response(ser.data, status=status.HTTP_201_CREATED)

        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        #查询集需要根据某个条件排序后，才能继续查询和分页
        queryset = self.get_queryset().order_by('id')
        filter_cate = request.GET.get('cate_id')
        filter_state = request.GET.get('state')
        if filter_state:
            queryset = queryset.filter(state=filter_state)

        if filter_cate:
            article_ids = IntermediateArticleCate.objects.filter(
                cate_id=filter_cate).values_list('article_id', flat=True)
            queryset = queryset.filter(id__in=article_ids)

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return Response(ser.data)
        return Response([])


class Article(GenericViewSet):
    queryset = ArticleStore.objects.all()
    serializer_class = ArticlesSerializer

    def update(self,request):
        data = request.data.copy()
        article = ArticleStore.objects.get(id=data['id'])
        username = request.user.username
        user = UserStore.objects.get(username=username)
        data['author_id'] = user.id
        data['pub_date'] = article.pub_date
        #提取旧图片地址 以备后续删除旧图片用
        cover_old = article.cover_img

        ser = ArticlesSerializer(article, data=data)

        if ser.is_valid():
            ser.save()

            intermediate = IntermediateArticleCate.objects.get(
                article_id=data['id'])
            serinter = ArticleCateSerializer(intermediate, data=data)
            if serinter.is_valid():
                serinter.save()

                cover_img_file = request.FILES.get('cover_img')
                if cover_img_file:
                    path = os.path.join(MEDIA_ROOT, 'img', cover_img_file.name)
                    default_storage.save(path, ContentFile(cover_img_file.read()))

                    #新图片保存成功，删除旧图片
                    path_old = os.path.join(MEDIA_ROOT, 'img',
                                            cover_old.path)
                    if path_old:
                        if os.path.exists(path_old):
                            os.remove(path_old)
                        else:
                            return Response('您要删除的图片未保存到数据库中')

                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                print(serinter.errors)
                return Response(serinter.errors, status=status.HTTP_201_CREATED)
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request):
        id = request.GET.get('id')
        article = ArticleStore.objects.select_related('author_id').get(
            id=id)
        #注意虽然数据库中是cate_id,但要按照模型类中的定义来
        inter = IntermediateArticleCate.objects.select_related('cate').get(
            id=id)
        user = article.author_id
        #注意虽然数据库中是cate_id,但要按照模型类中的定义来
        cate = inter.cate
        article.username = user.username
        article.nickname = user.nickname
        article.cate_id = cate.id
        article.cate_name = cate.cate_name
        article.cate_alias = cate.cate_alias

        ser = self.get_serializer(article)
        return Response(ser.data)

    def destroy(self, request):
        id = request.GET.get('id')
        try:
            article = ArticleStore.objects.get(id=id)
        except ArticleStore.DoesNotExist:
            return Response({'code': 1, 'message': '您要删除的文章不存在'}, status=status.HTTP_200_OK)

        cover_old = article.cover_img
        path_old = os.path.join(MEDIA_ROOT, 'img',
                                cover_old.path)
        article.delete()
        if path_old:
            if os.path.exists(path_old):
                os.remove(path_old)
                return Response(path_old)
            else:
                return Response({'code': 1, 'message': '您要删除的图片不存在'}, status=status.HTTP_200_OK)
        return Response({'code': 0, 'message': '删除成功！'}, status=status.HTTP_200_OK)
