from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from exposition.models import (ExpoStore, ExpoStaticData,
                               IntermediateExpoSector, IntermediateExpoTheme,
                               ExpoExhibitorStore)
from modeltranslation.translator import register, TranslationOptions


# Register your models here.
admin.site.register(ExpoStore)
admin.site.register(ExpoStaticData)
admin.site.register(ExpoExhibitorStore)
admin.site.register(IntermediateExpoSector)
admin.site.register(IntermediateExpoTheme)


# admin.site.register(ExpoName, ExpoNameAdmin)
# admin.site.register(ExpoDescription, ExpoDescriptionAdmin)
# class ExpoNameAdmin(TranslationAdmin):
#     pass
#
#
# @register(ExpoStaticData)
# class ExpoStaticDataTranslationOptions(TranslationOptions):
#     fields = ('name',)
#
#
# class ExpoDescriptionAdmin(TranslationAdmin):
#     pass
#
#
# @register(ExpoStore)
# class ExpoStoreTranslationOptions(TranslationOptions):
#     fields = ('description',)