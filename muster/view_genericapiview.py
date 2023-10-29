##################################################
#基本类视图(2)GenericAPIView--代码案例
##################################################

from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView

from books.models import BookInfo
from books_drf.serializer import BooksSerializer

#Books_drf负责多条数据的查找和新增
class Books_drf(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer

    # 查找多条数据
    def get(self,request):
        books = self.get_queryset()
        ser= self.get_serializer(books, many=True)
        return Response(ser.data)

    #新增一条数据
    def post(self,request):
        data = request.data
        ser = self.get_serializer(data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

#Book_drf负责单条数据的查找 修改和删除
class Book_drf(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer

    # 查找一条数据
    def get(self, request, pk):
        try:
            book = self.get_object()
        except:
            return JsonResponse({'error': '错误信息'}, status=400)
        ser = BooksSerializer(book)
        return Response(ser.data)

    # 修改一条数据
    def put(self, request, pk):
        data=request.data
        try:
            book = self.get_object()
        except:
            return JsonResponse({'error': '错误信息'}, status=400)
        ser = BooksSerializer(book, data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    # 删除一条数据
    def delete(self, request, pk):
        try:
            book = self.get_object()
        except:
            return Response({'error': '错误信息'}, status=400)
        book.delete()
        return Response({})