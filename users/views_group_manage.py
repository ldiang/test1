from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import UserStore
from users.serializer import GroupSerializer


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class GroupManage(ViewSet):
    def create(self, request):
        groupname = request.data.get('groupname')
        if not groupname:
            return Response({"code": 1, "message": "请提供分组名称"})
        try:
            group, created = Group.objects.get_or_create(name=groupname)
            if created:
                return Response({"code": 0, "message": "用户分组添加成功",
                                 "group_name": group.name})
            else:
                return Response({"code": 1, "message": "分组已存在"})
        except IntegrityError:
            return Response({"code": 1, "message": "分组创建失败"})

    def destroy(self, request):
        groupid = request.data.get('id')
        if not groupid:
            return Response({"code": 1, "message": "请确定要删除的分组"})
        try:
            group = Group.objects.get(id=groupid)
            group.delete()
            return Response({"code": 0, "message": "分组已删除"})
        except ObjectDoesNotExist:
            return Response({"code": 1, "message": "该分组不存在"})
        except IntegrityError:
            return Response({"code": 1, "message": "删除分组时出错"})

    def list(self, request):
        grouplist = Group.objects.all()
        ser = GroupSerializer(grouplist, many=True)

        return Response(ser.data)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class GroupAssign(GenericViewSet):
    def update(self,request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        try:
            user = UserStore.objects.get(pk=user_id)
            group = Group.objects.get(pk=group_id)
            #用户指定分组信息保存位置在userstore_group表单内
            user.groups.add(group)
            return Response({"code": 0, "message": "用户分配到用户组成功"})
        except UserStore.DoesNotExist:
            return Response({"code": 1, "message": "用户不存在"})
        except Group.DoesNotExist:
            return Response({"code": 1, "message": "用户组不存在"})






