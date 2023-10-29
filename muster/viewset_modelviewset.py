from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from books.models import BookInfo
from books_drf.serializer import BooksSerializer


class Books_drf(ModelViewSet):
    # 因为ModelViewSet继承了GenericAPIVIew和五个拓展类，所以这两行再配合路由就可以实现增删改查的功能
    queryset = BookInfo.objects.all()
    # serializer_class = BooksSerializer

    # 重写ModelViewSet中继承方法的意义
    # 例如针对不同的动作 指定不同的序列化器
    def get_serializer_class(self):
        if self.action == 'lastdata':
            return BooksSerializer
        elif self.action == 'create':
            return BooksSerializer
        else:
            return BooksSerializer

    @action(methods=['get'], detail=True)
    def lastdata(self, request, pk):
        print(self.action)
        book = BookInfo.objects.get(id=pk)
        ser = self.get_serializer(book)
        return Response(ser.data)
