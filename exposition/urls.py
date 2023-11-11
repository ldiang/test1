from django.urls import path,re_path

from . import views

urlpatterns = [
    path('staticinfolist/', views.ExpoStaticInfoList.as_view({'post': 'create', 'delete': 'destroy', 'get': 'list'})),
    path('staticinfo/', views.ExpoStaticInfo.as_view(
        {'get': 'retrieve','put': 'update'})),

    # path('list/', views.Articles.as_view({'get': 'list'})),
    #
    # path('info/', views.Article.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),
    # #path('pic/', views.PicUpload.as_view({'post': 'create'})),

]