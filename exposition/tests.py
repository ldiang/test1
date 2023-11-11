from django.test import TestCase
from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your tests here.
class ExpoSector(models.Model):
    sector = models.CharField(max_length=255)
    parent_sector = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    sector_words = JSONField(default=dict)

    def add_sector_word(self, lang_code, word):
        # 添加机器人单词到字典中
        self.sector_words[lang_code] = word