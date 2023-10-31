from django.db import models
from django.contrib.auth.models import Group


# Create your models here.
class LayoutSidebar(models.Model):
    id = models.BigAutoField(primary_key=True)
    index_path = models.CharField(max_length=50)
    title = models.CharField(max_length=10)
    icon = models.CharField(max_length=100)
    path_level = models.IntegerField()
    parent_path = models.ForeignKey('self', on_delete=models.SET_NULL,
                                    null=True)
    auth_group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        db_table = 'front_sidebar'
        verbose_name = '前端侧边栏'
        verbose_name_plural = verbose_name
