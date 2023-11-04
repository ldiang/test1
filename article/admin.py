from django.contrib import admin

from article.models import ArticleStore, ArticleCateIntermediate

# Register your models here.
admin.register(ArticleStore),
admin.register(ArticleCateIntermediate)