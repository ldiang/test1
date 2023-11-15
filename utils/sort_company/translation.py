from modeltranslation.translator import register, TranslationOptions

from utils.sort_company.models import SortCompanyStore


@register(SortCompanyStore)
class SortCompanyStoreTranslationOptions(TranslationOptions):
    fields = ('description',)