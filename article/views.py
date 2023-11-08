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
from article_cate.models import ArticleCateStore
from article.models import ArticleStore, ArticleCateIntermediate
from article.serializer import ArticlesSerializer, ArticleCateSerializer
import os



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
        print(request.POST)
        username = request.user.username
        user = UserStore.objects.get(username=username)

        pub_date = datetime.now()

        data['author_id'] = user.id
        data['pub_date'] = pub_date
        ser = self.get_serializer(data=data)

        if ser.is_valid():
            ser.save()

            ##############################################

            new_article = ArticleStore.objects.get(title=data['title'],
                                                   id=ser.instance.id)
            new_cate_ids = [int(cate_id) for cate_id in
                            request.POST.getlist('cate_id')]
            print(new_cate_ids)

            new_cate_list = ArticleCateStore.objects.filter(id__in=new_cate_ids)

            for cate in new_cate_list:
                new_intermediate = [{'article': new_article.id, 'cate': cate.id}]

                print(new_intermediate)
                new_res = ArticleCateSerializer(data=new_intermediate, many=True)

                if new_res.is_valid():
                    new_res.save()
                else:
                    print(new_res.errors)

            return Response({"code": 0,
                             "message": "发布文章成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # 查询集需要根据某个条件排序后，才能继续查询和分页
        queryset = self.get_queryset().order_by('-pub_date')
        # 获取ArticleStore对象，并预获取相关的CateStore
        # article_data = ArticleStore.objects.prefetch_related(
        #     'articleCateIntermediate_set__cate').order_by('-pub_date')

        filter_cate = request.GET.get('cate_id')
        filter_state = request.GET.get('state')
        if filter_state and filter_state.strip():
            queryset = queryset.filter(state=filter_state)

        if filter_cate and filter_cate.strip():
            # article_ids = IntermediateArticleCate.objects.filter(
            #     cate_id=filter_cate).values_list('article_id', flat=True)
            # queryset = queryset.filter(id__in=article_ids)
            queryset = queryset.filter(cate_id=filter_cate)

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            # return Response(ser.data)
            return Response({"code": 0,
                             "message": "获取文章列表成功！",
                             "data": ser.data,
                             "total": queryset.count()})


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
            path_old = os.path.join(MEDIA_ROOT, 'img',
                                    cover_old.path)
        # 将cover_img剔除，防止前端没有传来图片而报错
        # if "cover_img" in data:
        #     del data["cover_img"]

        ser = ArticlesSerializer(article, data=data)
        if ser.is_valid():
            ser.save()
            # 这个条件判断很值得记住，根据过滤条件查询模型，然后用exists输出是否存在
            if ArticleCateIntermediate.objects.filter(
                    article=data['id']).exists():
                intermediate = ArticleCateIntermediate.objects.get(
                    article=data['id'])
                ser_inter = ArticleCateSerializer(intermediate, data=data)
                if ser_inter.is_valid():
                    ser_inter.save()
                else:
                    print(ser_inter.errors)
                    return Response(ser_inter.errors,
                                    status=status.HTTP_201_CREATED)
            else:
                new_inter = {'article_id': data['id'],
                             'cate_id': data['cate_id']}
                print(new_inter)
                new_inter_ser = ArticleCateSerializer(data=new_inter)
                if new_inter_ser.is_valid():
                    new_inter_ser.save()
                else:
                    print(ser.errors)

            # 保存上传图片
            # cover_img_file = request.FILES.get('cover_img')
            # print('图片文件名', cover_img_file.name)
            # if cover_img_file:
            #     path_new = os.path.join(BASE_DIR, 'media', 'img', cover_img_file.name)
            #     print('保存地址', path_new)
            #     default_storage.save(path_new,
            #                          ContentFile(cover_img_file.read()))
            if path_old is not None:
                if os.path.exists(path_old):
                    os.remove(path_old)

            return Response({"code": 0,
                             "message": "修改文章成功！",
                             "data": ser.data})
        else:
            print(ser.errors)
            return Response({"code": 1,
                             "message": "编辑文章失败，请修正输入内容",
                             "data": ser.data})

    def retrieve(self, request):
        id = request.GET.get('id')
        article = ArticleStore.objects.select_related('author_id').get(
            id=id)
        print(id)
        # 注意虽然数据库中是cate_id,但要按照模型类中的定义来
        try:
            inter = ArticleCateIntermediate.objects.select_related(
                'article').get(article=id)
            # 注意虽然数据库中是cate_id,但要按照模型类中的定义来
            cate = inter.cate
            article.cate_id = cate.id
            article.cate_name = cate.cate_name
            article.cate_alias = cate.cate_alias
        except:
            pass
        user = article.author_id
        article.username = user.username
        article.nickname = user.nickname

        ser = self.get_serializer(article)
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
            if os.path.exists(path_old):
                os.remove(path_old)
        article.delete()
        return Response({'code': 0, 'message': '删除成功！'},
                        status=status.HTTP_200_OK)
