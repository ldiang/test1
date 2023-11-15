from django.db import models

from utils.db_general_models.models import UtilCountry, UtilCity, UtilSector, \
    UtilTheme


# Create your models here.
class SortCompanyStore(models.Model):
    name = models.CharField(max_length=255,unique=True)
    country = models.ForeignKey(UtilCountry, on_delete=models.PROTECT)
    city = models.ForeignKey(UtilCity, on_delete=models.PROTECT)
    website = models.URLField()
    description = models.TextField(max_length=4000, null=True, blank=True)
    established = models.IntegerField(null=True, blank=True)
    num_staff = models.IntegerField(null=True, blank=True)
    sector = models.ManyToManyField(UtilSector,
                                    through='IntermediateCompanySector')
    theme = models.ManyToManyField(UtilTheme,
                                   through='IntermediateCompanyTheme')

    class Meta:
        db_table = 'sort_company'
        verbose_name = '企业'
        verbose_name_plural = verbose_name


class IntermediateCompanySector(models.Model):
    company = models.ForeignKey(SortCompanyStore, on_delete=models.CASCADE)
    sector = models.ForeignKey(UtilSector, on_delete=models.PROTECT)

    class Meta:
        db_table = 'intermediate_company_sector'
        verbose_name = '企业及行业中间表'
        verbose_name_plural = verbose_name


class IntermediateCompanyTheme(models.Model):
    company = models.ForeignKey(SortCompanyStore, on_delete=models.CASCADE)
    theme = models.ForeignKey(UtilTheme, on_delete=models.PROTECT)

    class Meta:
        db_table = 'intermediate_company_theme'
        verbose_name = '企业及热门主题中间表'
        verbose_name_plural = verbose_name