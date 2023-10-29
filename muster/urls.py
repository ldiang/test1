from django.urls import re_path
from . import (views, view_apiview, view_genericapiview, view_mixinview,view_mixinchildview, viewset_viewset,
               viewset_genericviewset, viewset_modelviewset, View_other_filter, View_other_ordering,
               View_other_pagination)
from rest_framework.routers import SimpleRouter

urlpatterns = [
    #re_path(r'^books_drf/$', views.Books_drf.as_view()),
    #re_path(r'^books_drf/(?P<pk>\d+)/$', views.Books_drf.as_view()),

    #DRF框架 Django View下的视图
    #re_path(r'^$', views.Books_drf.as_view(), name='books_drf_list'),
    #re_path(r'^(?P<pk>\d+)/$', views.Books_drf.as_view(), name='books_drf_detail'),

    #DRF框架 APIView
    #re_path(r'^$', view_apiview.Books_drf.as_view()),                       #利用Books_drf视图处理查询和增加
    #re_path(r'^(?P<pk>\d+)/$', view_apiview.Book_drf.as_view()),            #利用Book_drf视图处理单一数据的修改 删除

    # DRF框架 GenericApiView
    #re_path(r'^$', view_genericapiview.Books_drf.as_view()),
    #re_path(r'^(?P<pk>\d+)/$', view_genericapiview.Book_drf.as_view()),

    # DRF框架 5个拓展类视图
    #re_path(r'^$', view_mixinview.Books_drf.as_view()),
    #re_path(r'^(?P<pk>\d+)/$', view_mixinview.Book_drf.as_view()),

    # DRF框架 9个拓展类子类视图
    #re_path(r'^$', view_mixinchildview.Books_drf.as_view()),
    #re_path(r'^(?P<pk>\d+)/$', view_mixinchildview.Book_drf.as_view()),

    # DRF框架 视图集ViewSet
    # re_path(r'^$', viewset_viewset.Books_drf.as_view({'get':'list','post':'create'})),
    # re_path(r'^(?P<pk>\d+)/$', viewset_viewset.Book_drf.as_view({'get':'retrieve','put':'update','delete':'destroy'})),

    # DRF框架 视图集GenericViewSet
    # re_path(r'^$', viewset_genericviewset.Books_drf.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<pk>\d+)/$',
    #         viewset_genericviewset.Book_drf.as_view({'put': 'update', 'delete': 'destroy'})),
    # re_path(r'^(?P<pk>\d+)/lastdata/$', viewset_genericviewset.Book_drf.as_view({'get': 'lastdata'})),

    # DRF框架 视图集ModelViewSet  (注意这里获取单一对象用的视图也是Books_drf)
    # re_path(r'^$', viewset_modelviewset.Books_drf.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<pk>\d+)/$',
    #         viewset_modelviewset.Books_drf.as_view({'put': 'update', 'delete': 'destroy'})),
    # re_path(r'^(?P<pk>\d+)/lastdata/$', viewset_modelviewset.Books_drf.as_view({'get': 'lastdata'})),

    # DRF框架 基于视图集视图集ModelViewSet 过滤功能
    # re_path(r'^$', View_other_filter.Books_drf.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<pk>\d+)/$',
    #         View_other_filter.Books_drf.as_view({'put': 'update', 'delete': 'destroy'})),
    # re_path(r'^(?P<pk>\d+)/lastdata/$', View_other_filter.Books_drf.as_view({'get': 'lastdata'})),

    # DRF框架 基于视图集视图集ModelViewSet 排序功能
    # re_path(r'^$', View_other_ordering.Books_drf.as_view(
    #     {'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<pk>\d+)/$',
    #         View_other_ordering.Books_drf.as_view(
    #             {'put': 'update', 'delete': 'destroy'})),
    # re_path(r'^(?P<pk>\d+)/lastdata/$',
    #         View_other_ordering.Books_drf.as_view({'get': 'lastdata'})),

    # DRF框架 基于视图集视图集ModelViewSet 分页功能
    # re_path(r'^$', View_other_pagination.Books_drf.as_view(
    #     {'get': 'list', 'post': 'create'})),
    # re_path(r'^(?P<pk>\d+)/$',
    #         View_other_pagination.Books_drf.as_view(
    #             {'put': 'update', 'delete': 'destroy'})),
    # re_path(r'^(?P<pk>\d+)/lastdata/$',
    #         View_other_pagination.Books_drf.as_view({'get': 'lastdata'})),
]

#router = SimpleRouter()
#router.register('', View_other_pagination.Books_drf, basename='books')
#print(router.urls)
#urlpatterns += router.urls