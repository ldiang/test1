# Generated by Django 4.2 on 2023-11-03 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCateStore',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cate_name', models.CharField(max_length=20)),
                ('cate_alias', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'store_article_cate',
            },
        ),
    ]
