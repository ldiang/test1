from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from article_cate.models import ArticleCateStore
from users.models import UserStore


from article_cate.serializer import CatesSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Cates(GenericViewSet):
    queryset = ArticleCateStore.objects.all()
    serializer_class = CatesSerializer

    def create(self, request):
        data = request.data
        username = request.user.username
        user = UserStore.objects.get(username=username)
        data['creator_id'] = user.id
        ser = self.get_serializer(data=data)
        ser.is_valid()
        ser.save()
        #return Response(ser.data)
        return Response({"code": 0,
                         "message": "新增文章分类成功！",
                         "data": ser.data})
    def list(self, request):
        cates = self.get_queryset()
        ser = self.get_serializer(cates, many=True)
        #return Response(ser.data)
        return Response({"code": 0,
                         "message": "获取文章分类列表成功！",
                         "data": ser.data})

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Cate(GenericViewSet):
    def retrieve(self,request):
        try:
            id = request.GET.get('id')
            cate=ArticleCateStore.objects.get(id=id)
            ser=CatesSerializer(cate)
            #return Response(ser.data)
            return Response({"code": 0,
                             "message": "获取文章分类成功！",
                             "data": ser.data})
        except:
            return Response({"code": 1,
                             "message": "您查询的文章分类不存在！"})

    def update(self,request):
        data = request.data
        id = data['id']
        cate = ArticleCateStore.objects.get(id=id)
        ser = CatesSerializer(cate, data=data)
        ser.is_valid()
        ser.save()
        #return Response(ser.data)

        return Response({"code": 0,
                         "message": "更新分类信息成功！",
                         "data": ser.data})

    def destroy(self, request):
        id = request.GET.get('id')
        print(id)
        cate = ArticleCateStore.objects.get(id=id)
        cate.delete()
        return Response({"code": 0,
                        "message": "删除文章分类成功！"})


