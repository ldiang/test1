from django.db import models


# Create your models here.
class UtilLang(models.Model):
    lang_iso = models.CharField(max_length=255,unique=True)
    lang_cn = models.CharField(max_length=255)
    lang_code639 = models.CharField(max_length=255)


    class Meta:
        db_table = 'util_lang'
        verbose_name = '语言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.lang_cn


class UtilCountry(models.Model):
    country_en = models.CharField(max_length=255,unique=True)
    country_cn = models.CharField(max_length=255,unique=True)
    short_Len2 = models.CharField(max_length=20,unique=True)
    region = models.CharField(max_length=20, null=True,unique=True)


    class Meta:
        db_table = 'util_country'
        verbose_name = '国家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.country


class UtilCity(models.Model):
    city_en = models.CharField(max_length=255,unique=True)
    city_cn = models.CharField(max_length=255,unique=True)
    country = models.ForeignKey(UtilCountry, on_delete=models.PROTECT,
                             null=True)


    class Meta:
        db_table = 'util_city'
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city
