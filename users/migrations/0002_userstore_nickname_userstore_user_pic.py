# Generated by Django 4.2 on 2023-10-29 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstore',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='userstore',
            name='user_pic',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='头像'),
        ),
    ]
