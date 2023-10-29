from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter    #第1步 导入过滤器

from books.models import BookInfo
from books_drf.serializer import BooksSerializer




class Books_drf(ModelViewSet):
    queryset = BookInfo.objects.all()
    # serializer_class = BooksSerializer

    # 第2步 指定排序方法类
    filter_backends = [OrderingFilter]
    # 第3步 指定排序字段
    ordering_fields=('id','bread')



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
