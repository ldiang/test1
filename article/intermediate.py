from django.db import models

from article.models import ArticleStore
from cate_article.models import CateStore


class IntermediateArticleCate(models.Model):
    article = models.ForeignKey(ArticleStore, on_delete=models.CASCADE)
    cate = models.ForeignKey(CateStore, on_delete=models.CASCADE)

    class Meta:
        db_table = 'intermediate_article_cate'
        verbose_name = '文章及所属分类中间表'
        verbose_name_plural = verbose_name
