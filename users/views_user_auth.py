from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from users.models import UserStore


class UserIsSuperuser(GenericViewSet):
    def update(self, request):
        if request.user.is_superuser:
            user_id = request.data.get('user_id')
            is_superuser = request.data.get('is_superuser')

            try:
                user = UserStore.objects.get(id=user_id)
                user.is_superuser = bool(is_superuser)
                user.save()
                return Response({"code": 0, "message": "用户权限修改成功"})
            except UserStore.DoesNotExist:
                return Response({"code": 1, "message": "用户不存在"})
        else:
            return Response({"code": 1, "message": "您没有权限修改超级管理员"})

