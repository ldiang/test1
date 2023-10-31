from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from front_sidebar.models import LayoutSidebar
from front_sidebar.serializer import SidebarSerializer


class Sidebar(ViewSet):

    def list(self, request):
        data = LayoutSidebar.objects.all()
        ser = SidebarSerializer(data, many=True)
        result = self.build_menu_structure(ser.data)
        return Response({
            "code": 0,
            "message": "获取左侧菜单成功！",
            "data": result
        })

    def create(self, request):
        data = request.data.copy()

        try:
            LayoutSidebar.objects.get(title=data['title'])
            return Response({"code": 1, "message": "路由必须是唯一值"})
        except ObjectDoesNotExist:
            if data['auth_group'] is None or data['auth_group'] == '':
                data['auth_group'] = 1
            # 需要处理parent_path为空字符的
            print(data)
            ser = SidebarSerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response({"code": 0,
                                 "data": ser.data,
                                 "message": "为侧边栏成功设置新内容"})
            else:
                print(ser.errors)
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def build_menu_structure(self, data, parent_id=None):
        menu_structure = []
        #注意:item是OrderedDict，所以需要item.get('parent_path')才能得到数据
        for item in data:
            if item.get('parent_path') == parent_id:
                menu_item = {
                    "indexPath": item.get('index_path'),
                    "title": item.get('title'),
                    "icon": item.get('icon')
                }
                children = self.build_menu_structure(data, item.get('id'))
                if children:
                    menu_item["children"] = children
                menu_structure.append(menu_item)

        return menu_structure

    # parent_id 参数表示当前正在处理的父菜单项的 ID。初始值为None，以处理顶级菜单项
    # 代码遍历数据的每一项，注意数据是类似字典的OrderedDict
    # 注意初始父级菜单是列表
    # 对于每个菜单项，代码检查其parent_path值是否与当前处理的父菜单项的ID匹配。
    # 如果parent_path值匹配，说明当前的菜单项是当前父菜单项的子菜单项。
    # 将为该菜单项创建一个字典(包含indexPath title icon)，这个菜单的字典将被添加到父级菜单的列表中
    # 通过递归调用build_menu_structure，数据列表和当前子菜单项的 id 作为参数传递，寻找当前菜单的子菜单。
    # 如果存在子菜单项（即 children 列表非空），将子菜单项添加到当前菜单项的 children 下，构建嵌套的菜单结构。
    # 递归继续，直到没有匹配的子菜单项或没有更多的层次结构。然后，菜单结构返回到上一级的父菜单项。
    # 最终，整个递归过程将生成一个嵌套的菜单结构，其中每个菜单项都包含其子菜单项。这个结构可以用于构建具有层次结构的菜单或导航。