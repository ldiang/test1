from django.urls import path,re_path

from utils.db_general_models import views

urlpatterns = [
    path('lang/', views.DB_Manage_Lang.as_view({'post': 'create', 'get': 'list'})),

    path('country/',
         views.DB_Manage_country.as_view({'post': 'create', 'get': 'list'})),
    #
    path('city/',
         views.DB_Manage_city.as_view({'post': 'create', 'get': 'list','delete': 'destroy'})),

    path('sector/',
         views.DB_Manage_sector.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'})),

    path('sector/rebuild/',
         views.DB_Manage_sector_rebuild.as_view(
             {'get': 'list'})),

    path('theme/',
         views.DB_Manage_theme.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'})),
    #path('list/', views.Articles.as_view({'get': 'list'})),

    #path('info/', views.Article.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),

]