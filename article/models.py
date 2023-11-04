from django.db import models

from article_cate.models import ArticleCateStore
from users.models import UserStore


class ArticleStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    state = models.CharField(max_length=10,
                             choices=[("已发布", "已发布"), ("草稿", "草稿")])
    cover_img = models.ImageField(upload_to='img/', blank=True, null=True)
    author_id = models.ForeignKey(UserStore, on_delete=models.SET_NULL,
                                  null=True)
    cate_id = models.ManyToManyField(ArticleCateStore,
                                     through='ArticleCateIntermediate')
    pub_date = models.DateTimeField()

    class Meta:
        db_table = 'store_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ArticleCateIntermediate(models.Model):
    article = models.ForeignKey(ArticleStore, on_delete=models.CASCADE)
    cate = models.ForeignKey(ArticleCateStore, on_delete=models.CASCADE)

    class Meta:
        db_table = 'intermediate_article_cate'
        verbose_name = '文章及所属分类中间表'
        verbose_name_plural = verbose_name