from django.views import View
from books.models import BookInfo  # 从另一子应用中导入模型类
from books_drf.serializer import BooksSerializer
from django.http import JsonResponse


# Create your views here.
class Books_drf(View):

    def get(self, request):
        books = BookInfo.objects.all()
        ser = BooksSerializer(books, many=True)
        return JsonResponse(ser.data, safe=False)
