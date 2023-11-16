from django.urls import path,re_path

from utils.sort_company import views

urlpatterns = [
    path('manage/',
         views.SortCompaniesAction.as_view({'post': 'create', 'get': 'list'})),
    path('manage/details/',
         views.SortCompanyAction.as_view({'post': 'create', 'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # path('info/', views.Article.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),

]