##################################################
# 5个拓展类视图--代码案例
##################################################

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from books.models import BookInfo
from books_drf.serializer import BooksSerializer


# Books_drf负责多条数据的查找和新增
class Books_drf(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer

    # 查找多条数据
    def get(self, request):
        return self.list(request)

    # 新增一条数据
    def post(self, request):
        return self.create(request)


# Book_drf负责单条数据的查找 修改和删除
class Book_drf(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer

    # 查找一条数据
    def get(self, request, pk):
        return self.retrieve(request, pk)

    # 修改一条数据
    def put(self, request, pk):
        return self.update(request, pk)

    # 删除一条数据
    def delete(self, request, pk):
        return self.destroy(request, pk)
