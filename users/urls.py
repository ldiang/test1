from django.urls import path,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views, views_group_manage, views_user_auth

urlpatterns = [
    path('reg', views.UserCreate.as_view({'post': 'create'})),
    path('login', views.UserLogin.as_view({'post': 'create'})),
    path('userlist/', views.UserList.as_view({'get': 'list'})),
    #上面三个是测试用
    #修改 及 获取 用户信息
    path('userinfo/', views.UserInfo.as_view({'get': 'retrieve', 'put': 'update'})),
    #更新用户密码
    path('updatepwd',
         views.UserPasswordReset.as_view({'put': 'update'})),
    #更新头像
    path('update/avatar/',
         views.UserInfo.as_view({'patch': 'partial_update'})),
    #新增 删除 和获取 分组信息
    path('group/manage',
         views_group_manage.GroupManage.as_view({'post': 'create',
                                                 'delete': 'destroy',
                                                 'get': 'list'})),
    #为用户指定分组
    path('group/userauth',
         views_group_manage.GroupAssign.as_view({'put': 'update'})),
    #为用户指定超级管理员权限
    path('userauth/superuser',
         views_user_auth.UserIsSuperuser.as_view({'put': 'update'}))

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
]