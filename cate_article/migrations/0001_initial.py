# Generated by Django 4.2 on 2023-10-29 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CateStore',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cate_name', models.CharField(max_length=20, verbose_name='名称')),
                ('cate_alias', models.CharField(max_length=20, verbose_name='发布日期')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'store_cate_article',
            },
        ),
    ]