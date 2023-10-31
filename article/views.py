import uuid
from datetime import datetime
from django.conf.global_settings import MEDIA_ROOT

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import UserStore
from cate_article.models import CateStore
from article.models import ArticleStore
from article.intermediate import IntermediateArticleCate
from article.serializer import ArticlesSerializer, ArticleCateSerializer
import os
from django.conf import settings


# Create your views here.
class ArticlesPaginator(PageNumberPagination):
    page_size = 8
    max_page_size = 20
    page_query_param = 'pagenum'
    page_size_query_param = 'pagesize'


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
            # 中间表
            # ser.instance 是序列化器保存数据后返回的模型实例。
            # 通过 id 过滤出唯一的 ArticleStore 对象
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
                #     cover_img_file = request.FILES.get('cover_img')
                #     if cover_img_file:
                #         path = os.path.join(MEDIA_ROOT, 'img', cover_img_file.name)
                #         default_storage.save(path, ContentFile(cover_img_file.read()))

                return Response({"code": 0,
                                 "message": "发布文章成功！",
                                 "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # 查询集需要根据某个条件排序后，才能继续查询和分页
        queryset = self.get_queryset().order_by('-pub_date')
        filter_cate = request.GET.get('cate_id')
        filter_state = request.GET.get('state')
        if filter_state and filter_state.strip():
            queryset = queryset.filter(state=filter_state)

        if filter_cate and filter_cate.strip():
            article_ids = IntermediateArticleCate.objects.filter(
                cate_id=filter_cate).values_list('article_id', flat=True)
            queryset = queryset.filter(id__in=article_ids)

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            # return Response(ser.data)
            return Response({"code": 0,
                             "message": "获取文章列表成功！",
                             "data": ser.data,
                             "total": queryset.count()})

        # return Response([])


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Article(GenericViewSet):
    queryset = ArticleStore.objects.all()
    serializer_class = ArticlesSerializer

    def update(self, request):
        data = request.data.copy()
        article = ArticleStore.objects.get(id=data['id'])
        username = request.user.username
        user = UserStore.objects.get(username=username)
        data['author_id'] = user.id
        data['pub_date'] = article.pub_date
        # 提取旧图片地址 以备后续删除旧图片用
        path_old = None
        if article.cover_img:
            cover_old = article.cover_img
            print(cover_old)
            path_old = os.path.join(MEDIA_ROOT, 'img',
                                    cover_old.path)
            print(path_old)
        ser = ArticlesSerializer(article, data=data)

        if ser.is_valid():
            ser.save()

            intermediate = IntermediateArticleCate.objects.get(
                article_id=data['id'])
            serinter = ArticleCateSerializer(intermediate, data=data)
            if serinter.is_valid():
                serinter.save()

                # cover_img_file = request.FILES.get('cover_img')
                # if cover_img_file:
                #     path = os.path.join(MEDIA_ROOT, 'img', cover_img_file.name)
                #     default_storage.save(path,
                #                          ContentFile(cover_img_file.read()))

                if os.path.exists(path_old):
                    os.remove(path_old)

                return Response({"code": 0,
                                 "message": "修改文章成功！",
                                 "data": ser.data})


            else:
                print(serinter.errors)
                return Response(serinter.errors, status=status.HTTP_201_CREATED)



                # return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            print(ser.errors)
            # return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"code": 1,
                             "message": "编辑文章失败，请修正输入内容",
                             "data": ser.data})

    def retrieve(self, request):
        id = request.GET.get('id')
        article = ArticleStore.objects.select_related('author_id').get(
            id=id)
        print(type(article))
        # 注意虽然数据库中是cate_id,但要按照模型类中的定义来
        # inter = IntermediateArticleCate.objects.select_related('article').get(id=id)
        inter = IntermediateArticleCate.objects.select_related('article').get(
            article=id)
        user = article.author_id
        # 注意虽然数据库中是cate_id,但要按照模型类中的定义来
        cate = inter.cate

        article.cate_id = cate.id
        article.cate_name = cate.cate_name
        article.cate_alias = cate.cate_alias
        article.username = user.username
        article.nickname = user.nickname

        ser = self.get_serializer(article)
        # return Response(ser.data)
        print(ser.data)
        return Response({"code": 0,
                         "message": "获取文章成功！",
                         "data": ser.data})

    def destroy(self, request):
        id = request.GET.get('id')
        try:
            article = ArticleStore.objects.get(id=id)
        except ArticleStore.DoesNotExist:
            return Response({'code': 1, 'message': '您要删除的文章不存在'},
                            status=status.HTTP_200_OK)

        if article.cover_img:
            cover_old = article.cover_img
            path_old = os.path.join(MEDIA_ROOT, 'img', cover_old.path)
            print(path_old)
            article.delete()
            if os.path.exists(path_old):
                os.remove(path_old)
            return Response({'code': 0, 'message': '删除成功！'},
                        status=status.HTTP_200_OK)


#######用于测试图片上传
class PicUpload(GenericViewSet):
    def create(self, request):
        cover_img_file = request.FILES.get('cover_img')
        if cover_img_file:
            path = os.path.join(MEDIA_ROOT, 'img', cover_img_file.name)
            default_storage.save(path, ContentFile(cover_img_file.read()))
            server_url = request.build_absolute_uri('/')
            # image_url = f'{server_url}media/img/{os.path.basename(path)}'
            image_url = f'{server_url}img/{os.path.basename(path)}'
            # 返回 JSON 格式的响应，包括图片 URL 和文件名
            response_data = {
                'code': 0,
                'message': '图标成功保存在服务器中',
                'url': image_url,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
