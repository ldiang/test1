from django.db import models
from cate_article.models import CateStore
from users.models import UserStore


# def upload_cover_img(instance, filename):
#     return 'media/img/{filename}'.format(filename=filename)

    # Create your models here.
class ArticleStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    state = models.CharField(max_length=10,
                             choices=[("已发布", "已发布"), ("草稿", "草稿")])
    cover_img = models.ImageField(upload_to='img/', blank=True, null=True)
    # cover_img = models.ImageField(upload_to=upload_cover_img, blank=True,
    # #                               null=True)

    # cate_id = models.ManyToManyField(CateStore, through=ArticleCate)
    author_id = models.ForeignKey(UserStore, on_delete=models.SET_NULL,
                                  null=True)
    pub_date = models.DateTimeField()

    class Meta:
        db_table = 'store_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
