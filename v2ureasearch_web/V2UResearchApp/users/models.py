from django.db import models
from ckeditor.fields import RichTextField

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
