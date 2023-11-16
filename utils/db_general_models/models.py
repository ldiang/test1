from django.db import models
from modeltranslation.translator import TranslationOptions, register


# Create your models here.
class UtilLang(models.Model):
    lang_iso = models.CharField(max_length=255, unique=True)
    lang_cn = models.CharField(max_length=255)
    lang_code639 = models.CharField(max_length=255)

    class Meta:
        db_table = 'util_lang'
        verbose_name = '语言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.lang_cn


class UtilCountry(models.Model):
    country_en = models.CharField(max_length=255, unique=True)
    country_cn = models.CharField(max_length=255, unique=True)
    short_Len2 = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=20, null=True)

    # @classmethod
    # #使用 Python 的 Unicode 编码范围来判断字符是否为中文字符。
    # # 中文字符的 Unicode 范围是 0x4e00 到 0x9fff。
    # def get_country_by_name(cls, name):
    #     if any('\u4e00' <= char <= '\u9fff' for char in name):
    #         # 中文名字，根据中文名字查询
    #         return cls.objects.filter(country_cn=name)
    #     else:
    #         # 英文名字，根据英文名字查询
    #         return cls.objects.filter(country_en=name)

    class Meta:
        db_table = 'util_country'
        verbose_name = '国家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.country_cn


class UtilCity(models.Model):
    city_en = models.CharField(max_length=255, unique=True)
    city_cn = models.CharField(max_length=255, unique=True,null=True)
    country = models.ForeignKey(UtilCountry, on_delete=models.PROTECT,
                                null=True)

    class Meta:
        db_table = 'util_city'
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city_en


class UtilSector(models.Model):
    sector = models.CharField(max_length=255, null=True)
    parent_sector = models.ForeignKey('self', null=True, blank=True,
                                      on_delete=models.PROTECT)

    class Meta:
        db_table = 'util_sector'
        verbose_name = '行业'
        verbose_name_plural = verbose_name
        unique_together = ['sector', 'parent_sector']

    def __str__(self):
        return self.sector


class UtilTheme(models.Model):
    theme = models.CharField(max_length=255, null=True)
    sector = models.ForeignKey(UtilSector, null=True, blank=True,
                               on_delete=models.PROTECT)

    class Meta:
        db_table = 'util_theme'
        verbose_name = '热门主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.theme
