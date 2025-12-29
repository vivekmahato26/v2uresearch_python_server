from django.contrib import admin
from .models import Package, Invoice, Payment

# Register your models here.

admin.site.register(Package)
admin.site.register(Invoice)
admin.site.register(Payment)