from django.contrib import admin
from .models import Pages, Blocks

# Register your models here.

class BlocksAdmin(admin.ModelAdmin):
    list_display = ["block_name", "region"]


admin.site.register(Pages)
admin.site.register(Blocks, BlocksAdmin)
