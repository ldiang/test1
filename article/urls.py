from django.urls import path,re_path

from . import views

urlpatterns = [
    path('add/', views.Articles.as_view({'post': 'create'})),
    path('list/', views.Articles.as_view({'get': 'list'})),

    path('info/', views.Article.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),
    #path('pic/', views.PicUpload.as_view({'post': 'create'})),

]