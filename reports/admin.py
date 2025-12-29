from django.contrib import admin
from reports.models import Report
from django.contrib.auth.models import User

# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display = ("title","get_sector")
    filter_horizontal = ('product', 'sector', 'company')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('product','author')

    def get_sector(self, obj):
            return "\n".join([s.sector_name for s in obj.sector.all()])
    
#admin.site.register(Report)
admin.site.register(Report, ReportAdmin)
