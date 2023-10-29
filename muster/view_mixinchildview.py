##################################################
# 拓展类视图的9个拓展类子类--代码案例
##################################################

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from books.models import BookInfo
from books_drf.serializer import BooksSerializer


# Books_drf负责多条数据的查找和新增
class Books_drf(ListCreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer


# Book_drf负责单条数据的查找 修改和删除
class Book_drf(RetrieveUpdateDestroyAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer
