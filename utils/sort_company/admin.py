from django.contrib import admin

from utils.sort_company.models import SortCompanyStore, \
    IntermediateCompanySector, IntermediateCompanyTheme

# Register your models here.
admin.site.register(SortCompanyStore)
admin.site.register(IntermediateCompanySector)
admin.site.register(IntermediateCompanyTheme)

