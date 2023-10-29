from django.db import models
from users.models import UserStore


# Create your models here.
class CateStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    cate_name = models.CharField(max_length=20, verbose_name='名称')
    cate_alias = models.CharField(max_length=20, verbose_name='发布日期')
    creator = models.ForeignKey(UserStore, on_delete=models.SET_NULL, null=True,
                              verbose_name='图书')  # 外键

    class Meta:
        db_table = 'store_cate_article'  # 指明数据库表名
        verbose_name = '文章分类'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
