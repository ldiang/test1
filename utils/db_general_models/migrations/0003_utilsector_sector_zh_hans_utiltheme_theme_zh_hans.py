# Generated by Django 4.2 on 2023-11-10 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_general_models', '0002_alter_utilsector_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilsector',
            name='sector_zh_Hans',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utiltheme',
            name='theme_zh_Hans',
            field=models.CharField(max_length=255, null=True),
        ),
    ]