from django.contrib import admin
from .models import place
from import_export.admin import ImportExportModelAdmin
# Register your models here
class DataImportExportAdmin(ImportExportModelAdmin):
    list_display = ('DBA', 'BORO', 'BUILDING', 'STERRT','ZIPCODE','PHONE','CUISION','LATITUDE','LONGTITUDE')
    
admin.site.register(place,DataImportExportAdmin)