from django.urls import path,re_path

from . import views

urlpatterns = [
    path('add/', views.Cates.as_view({'post': 'create'})),
    path('info/', views.Cates.as_view({'get': 'list'})),
]