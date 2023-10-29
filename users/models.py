from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserStore(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name='手机号')

    first_name = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name='姓')
    last_name = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name='名')
    email = models.CharField(max_length=254, blank=True, null=True, verbose_name='邮箱')
    is_superuser = models.BooleanField(default=False, blank=True, null=True, verbose_name='超级用户')
    is_staff = models.BooleanField(default=True, blank=True, null=True, verbose_name='员工')
    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name='是否在职')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='上次登陆时间')
    date_joined = models.DateTimeField(blank=True, null=True, verbose_name='创建账户时间')

    class Meta:
        db_table = 'userstore'  # 指明数据库表名
        verbose_name = '员工'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username
