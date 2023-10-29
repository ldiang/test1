from django.urls import path,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views




urlpatterns = [
    path('register/', views.UserCreate.as_view({'post': 'create'})),
    path('login/', views.UserLogin.as_view({'post': 'create'})),
    path('userlist/', views.UserList.as_view({'get': 'list'})),
    #上面三个是测试用，以下为正式路由
    path('userinfo/', views.UserInfo.as_view({'get': 'retrieve', 'put': 'update'})),


    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
]