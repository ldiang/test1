from django.contrib import admin

from article.intermediate import IntermediateArticleCate
from article.models import ArticleStore

# Register your models here.
admin.register(ArticleStore)
admin.register(IntermediateArticleCate)


