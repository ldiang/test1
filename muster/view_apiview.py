##################################################
#基本类视图(1)APIView--代码案例
##################################################

from rest_framework.response import Response

from rest_framework.views import APIView

from books.models import BookInfo
from books_drf.serializer import BooksSerializer

#Books_drf负责多条数据的查找和新增
class Books_drf(APIView):

    # 查找多条数据
    def get(self, request):
        books = BookInfo.objects.all()
        ser = BooksSerializer(books, many=True)     # 注意 返回多个值 需要many=True
        return Response(ser.data)

    #新增一条数据
    def post(self, request):
        newdata = request.data
        ser = BooksSerializer(data=newdata)
        ser.is_valid()

        ser.save()

        return Response(ser.data)

#Book_drf负责单条数据的查找 修改和删除
class Book_drf(APIView):

    # 查找一条数据
    def get(self, request, pk):
        book = BookInfo.objects.get(id=pk)
        ser = BooksSerializer(book)

        return Response(ser.data)

    # 修改一条数据
    def put(self, request, pk):
        data = request.data

        try:
            book = BookInfo.objects.get(id=pk)
        except:
            return Response({'error': '错误信息'}, status=400)

        ser = BooksSerializer(book, data=data)
        ser.is_valid()

        ser.save()

        return Response(ser.data)

    # 删除一条数据
    def delete(self, request, pk):
        # 1、查询数据对象
        try:
            book = BookInfo.objects.get(id=pk)

        except:
            return Response({'error': '错误信息'}, status=400)

        book.delete()

        return Response({})
