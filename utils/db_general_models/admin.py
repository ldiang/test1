from django.contrib import admin

from db_general_models.models import UtilLang, UtilCountry, UtilCity

# Register your models here.
admin.register(UtilLang)
admin.register(UtilCountry)
admin.register(UtilCity)
