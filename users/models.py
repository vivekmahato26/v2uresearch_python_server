from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    subscription_status = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    secondary_email = models.EmailField(max_length=200)
    secondary_phone = models.IntegerField(default=0)
    address = models.TextField()
    zip_code = models.CharField(max_length=200)
    income = models.EmailField()
    registered_device_1 = models.IntegerField(default=0)
    registered_device_2 = models.IntegerField(default=0)
    # product = models.ManyToManyField(Product)
    free_trial = models.BooleanField(default=False)
    expire_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class Region(models.Model):
    country_name = models.CharField(max_length=200)
    timezone = models.TimeField()
    country_code = models.CharField(max_length=200)
    currency = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    # additional attributes for dynamically
    corp_address = models.CharField(verbose_name="Corporation Address", max_length=255, default='', null=True, blank=True)
    corp_contact = models.CharField(verbose_name="Corporation Contact", max_length=25, default='', null=True, blank=True)
    corp_email = models.EmailField(verbose_name="Corporation Email", default='', null=True, blank=True)
    corp_text = models.CharField(verbose_name="Corporation Text", max_length=255, default='', null=True, blank=True)
    corp_number = models.CharField(verbose_name="Corporation Number", max_length=25, default='', null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    tradingview_exchange_code = models.CharField(verbose_name="TradingView Code", max_length=10, default='NYSE', null=True)
    region_hostname = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "Regions"
        verbose_name = "Region"
    
    def __str__(self):
        return self.country_name

class LoginsLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField()



"""
Users  --> done
Profile  -->
Products --> done
Packages --> done
Sectors
ResearchTypes
Reports
Invoices
Payments
Leads
LoginsLog
company

Users 1 ->- M LoginsLog
Users 1 ->- 1 Profile
Users 1 ->- M Packages
Packages 1 ->- 1 Invoices
Invoices 1 ->- M Payments

Packages 1 ->- M Products

Reports 1 ->- M Products
Reports 1 ->- M Sectors
Reports 1 ->- M ResearchTypes
"""

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
