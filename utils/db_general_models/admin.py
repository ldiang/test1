from django.contrib import admin
# 注意 模型类前面必须加utils,否则无法识别
from utils.db_general_models.models import UtilLang, UtilCountry, UtilCity, UtilSector, UtilTheme


# Register your models here.
admin.site.register(UtilLang)
admin.site.register(UtilCountry)
admin.site.register(UtilCity)
admin.site.register(UtilSector)
admin.site.register(UtilTheme)

