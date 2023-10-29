from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

# Create your views here.
from books_drf.serializer import BooksSerializer
from books.models import BookInfo


class Books_drf(ViewSet):
    def list(self, request):
        books = BookInfo.objects.all()
        ser = BooksSerializer(books, many=True)
        return Response(ser.data)

    def create(self, request):
        data = request.data
        ser = BooksSerializer(data=data)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

class Book_drf(ViewSet):
    def retrieve(self,request, pk):
        book = BookInfo.objects.get(id=pk)
        ser = BooksSerializer(book)
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




