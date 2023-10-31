from django.urls import path, re_path, include

urlpatterns = [

    path('admin/', include('users.urls')),
    path('my/cate/', include('cate_article.urls')),
    path('my/article/', include('article.urls')),

    path('my/', include('users.urls')),
    path('api/', include('users.urls')),

]