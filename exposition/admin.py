from django.contrib import admin

from exposition.models import (ExpositionStore, ExpoName, ExpoDate,
                               ExpoDescription, ExpoNum, ExpoVisit, ExpoSector,
                               ExpoTheme)

# Register your models here.
admin.register(ExpositionStore)
admin.register(ExpoName)
admin.register(ExpoDate)
admin.register(ExpoDescription)
admin.register(ExpoNum)
admin.register(ExpoVisit)
admin.register(ExpoSector)
admin.register(ExpoTheme)
