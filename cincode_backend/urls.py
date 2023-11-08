from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve

from django.conf.urls.static import static
urlpatterns = [

    path('admin/', include('users.urls')),
    path('my/cate/', include('article_cate.urls')),
    path('my/article/', include('article.urls')),
    path('my/menus', include('webmodule_sidebar.urls')),

    path('my/', include('users.urls')),
    path('api/', include('users.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)