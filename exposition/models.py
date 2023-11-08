from django.db import models

from utils.db_general_models.models import UtilLang, UtilCity, UtilCountry


class ExpoName(models.Model):
    name = models.CharField(max_length=255)
    lang = models.ForeignKey(UtilLang, on_delete=models.PROTECT,
                             null=True)

    class Meta:
        db_table = 'store_expo_name'
        verbose_name = '展会名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ExpoDate(models.Model):
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'store_expo_date'
        verbose_name = '展会日期'
        verbose_name_plural = verbose_name


class ExpoDescription(models.Model):
    descry = models.CharField(max_length=255)
    lang = models.ForeignKey(UtilLang, on_delete=models.PROTECT,
                             null=True)

    class Meta:
        db_table = 'store_expo_descry'
        verbose_name = '展会描述'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.descry


class ExpoNum(models.Model):
    num = models.IntegerField()

    class Meta:
        db_table = 'store_expo_num'
        verbose_name = '展商数量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.num


class ExpoVisit(models.Model):
    visit = models.IntegerField()

    class Meta:
        db_table = 'store_expo_visit'
        verbose_name = '展会访客数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.visit


class ExpoSector(models.Model):
    sector = models.CharField(max_length=255)
    parent_sector = models.ForeignKey('self', null=True, blank=True,
                                      on_delete=models.CASCADE)
    lang = models.ForeignKey(UtilLang, on_delete=models.PROTECT,
                             null=True)

    class Meta:
        db_table = 'store_expo_sector'
        verbose_name = '展会行业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sector


class ExpoTheme(models.Model):
    theme = models.CharField(max_length=255)
    lang = models.ForeignKey(UtilLang, on_delete=models.PROTECT,
                             null=True)

    class Meta:
        db_table = 'store_expo_theme'
        verbose_name = '展会热门主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.theme


# Create your models here.
class ExpositionStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.ForeignKey(ExpoName, on_delete=models.SET_NULL,
                             null=True)
    country = models.ForeignKey(UtilCountry, on_delete=models.SET_NULL,
                                null=True)
    city = models.ForeignKey(UtilCity, on_delete=models.SET_NULL,
                             null=True)
    next_date = models.ForeignKey(ExpoDate, on_delete=models.SET_NULL,
                                  null=True)
    descry = models.ForeignKey(ExpoDescription, on_delete=models.SET_NULL,
                               null=True)
    num_expo = models.ForeignKey(ExpoNum, on_delete=models.SET_NULL,
                                 null=True)
    num_visit = models.ForeignKey(ExpoVisit, on_delete=models.SET_NULL,
                                  null=True)
    sector = models.ForeignKey(ExpoSector, on_delete=models.SET_NULL,
                               null=True)
    theme = models.ForeignKey(ExpoTheme, on_delete=models.SET_NULL,
                              null=True)
    rating = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        db_table = 'store_expo'
        verbose_name = '展会'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
