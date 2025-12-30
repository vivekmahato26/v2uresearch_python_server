from django.contrib import admin
from users.models import User, Region, LoginsLog, UserProfile
from .forms import UserForm

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    form = UserForm

admin.site.register(User, UserAdmin)
admin.site.register(Region)
admin.site.register(LoginsLog)
admin.site.register(UserProfile)
