from django.urls import path, re_path, include

urlpatterns = [

    path('admin/', include('users.urls')),
    path('my/cate/', include('cate_article.urls')),
]