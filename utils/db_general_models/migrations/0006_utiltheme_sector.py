# Generated by Django 4.2 on 2023-11-13 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_general_models', '0005_alter_utilsector_sector_alter_utilsector_sector_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utiltheme',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='db_general_models.utilsector'),
        ),
    ]