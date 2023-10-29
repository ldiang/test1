from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination  # 第1步 导入

from books.models import BookInfo
from books_drf.serializer import BooksSerializer

class SetPagination(PageNumberPagination):                  # 第2步 定义分页类
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 3

class SetOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'xianzhi'
    offset_query_param = 'pianyi'
    max_limit =3

class Books_drf(ModelViewSet):
    queryset = BookInfo.objects.all()
    # serializer_class = BooksSerializer
    #pagination_class = PageNumberPagination                        # 第3步 指明pagination_class属性
    #pagination_class = LimitOffsetPagination
    pagination_class = SetOffsetPagination

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
