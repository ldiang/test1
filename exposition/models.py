from django.db import models

from utils.db_general_models.models import UtilLang, UtilCity, UtilCountry, \
    UtilSector, UtilTheme


# Create your models here.
# 在 ForeignKey 中使用 related_name： 简化反向查询
class ExpoStaticData(models.Model):
    name = models.CharField(max_length=255)
    # name = models.CharField(max_length=255,
    #                         default='The information will be released soon')
    country = models.ForeignKey(UtilCountry, on_delete=models.PROTECT)
    city = models.ForeignKey(UtilCity, on_delete=models.PROTECT)
    rating = models.IntegerField()
    website = models.URLField()

    class Meta:
        db_table = 'store_expo_staticdata'
        verbose_name = '展会基本信息'
        verbose_name_plural = verbose_name


class ExpoStore(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.ForeignKey(ExpoStaticData, on_delete=models.PROTECT,
                             related_name='this_expo', null=False, default=1)

    description = models.TextField(max_length=4000)

    date = models.DateField()

    num_expos = models.IntegerField()

    num_visit = models.IntegerField()

    sector = models.ManyToManyField(UtilSector,
                                    through='IntermediateExpoSector')
    theme = models.ManyToManyField(UtilTheme,
                                   through='IntermediateExpoTheme')

    class Meta:
        db_table = 'store_expo'
        verbose_name = '展会'
        verbose_name_plural = verbose_name


class IntermediateExpoSector(models.Model):
    expo = models.ForeignKey(ExpoStore, on_delete=models.CASCADE)
    sector = models.ForeignKey(UtilSector, on_delete=models.PROTECT)

    class Meta:
        db_table = 'intermediate_expo_sector'
        verbose_name = '展会及行业中间表'
        verbose_name_plural = verbose_name


class IntermediateExpoTheme(models.Model):
    expo = models.ForeignKey(ExpoStore, on_delete=models.CASCADE)
    theme = models.ForeignKey(UtilTheme, on_delete=models.PROTECT)

    class Meta:
        db_table = 'intermediate_expo_theme'
        verbose_name = '展会及热门主题中间表'
        verbose_name_plural = verbose_name
