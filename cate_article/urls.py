from django.urls import path,re_path

from . import views

urlpatterns = [
    path('add/', views.Cates.as_view({'post': 'create'})),
    path('list/', views.Cates.as_view({'get': 'list'})),

    path('info/', views.Cate.as_view({'get': 'retrieve', 'put': 'update'})),
    path('del/', views.Cate.as_view({'delete': 'destroy'})),

]