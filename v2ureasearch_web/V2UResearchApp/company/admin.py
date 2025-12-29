from django.contrib import admin
from .models import Sector, Company, ResearchTypes

# Register your models here.


class SectorAdmin(admin.ModelAdmin):
  list_display = ("sector_name",)
  prepopulated_fields = {"slug": ("sector_name",)}
  
admin.site.register(Sector, SectorAdmin)

admin.site.register(Company)
admin.site.register(ResearchTypes)

# Register your models here.
