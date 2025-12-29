from django.contrib import admin
from marketing.models import Product, Lead, Articles, SocialHandle

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Lead)
admin.site.register(Product, ProductAdmin)
admin.site.register(Articles)
admin.site.register(SocialHandle)
