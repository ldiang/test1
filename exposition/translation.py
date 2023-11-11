from modeltranslation.translator import register, TranslationOptions
from modeltranslation import translator
from modeltranslation.admin import TranslationAdmin

from exposition.models import ExpoStaticData, ExpoStore


@register(ExpoStaticData)
class ExpoStaticDataTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ExpoStore)
class ExpoStoreTranslationOptions(TranslationOptions):
    fields = ('description',)

# class ExpoStaticDataAdmin(TranslationAdmin):
#     pass
# class ExpoStoreAdmin(TranslationAdmin):
#     pass