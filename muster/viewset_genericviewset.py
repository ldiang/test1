from django.http import JsonResponse

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from books_drf.serializer import BooksSerializer
from books.models import BookInfo

class Books_drf(GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BooksSerializer

    def list(self, request):
        books = self.get_queryset()
        ser = self.get_serializer(books, many=True)
        return Response(ser.data)

    def create(self,request):
        data = request.data
        ser = self.get_serializer(data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

class Book_drf(GenericViewSet):

    def retrieve(self,request,pk):
        book=BookInfo.objects.get(id=pk)
        ser=BooksSerializer(book)
        return Response(ser.data)

    def update(self,request, pk):
        data = request.data
        book = BookInfo.objects.get(id=pk)
        ser = BooksSerializer(book, data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def destroy(self, request, pk):
        book = BookInfo.objects.get(id=pk)
        book.delete()
        return Response({})