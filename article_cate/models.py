from django.db import models
from users.models import UserStore


# Create your models here.
class ArticleCateStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    cate_name = models.CharField(max_length=20)
    cate_alias = models.CharField(max_length=20)
    creator = models.ForeignKey(UserStore, on_delete=models.SET_NULL, null=True)  # 外键

    class Meta:
        db_table = 'store_article_cate'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.cate_name