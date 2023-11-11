from modeltranslation.translator import register, TranslationOptions

from utils.db_general_models.models import UtilSector, UtilTheme


@register(UtilSector)
class UtilSectorTranslationOptions(TranslationOptions):
    fields = ('sector',)


@register(UtilTheme)
class UtilThemeTranslationOptions(TranslationOptions):
    fields = ('theme',)