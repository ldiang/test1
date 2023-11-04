from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.Sidebar.as_view({'post': 'create', 'get': 'list'})),
    #path('list/', views.Articles.as_view({'get': 'list'})),

    #path('info/', views.Article.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),

]