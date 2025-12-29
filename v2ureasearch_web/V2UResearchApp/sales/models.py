from django.db import models
from marketing.models import Product
from ckeditor.fields import RichTextField
from users.models import User
# from packages.models import Package

# Create your models here.

class Package(models.Model):
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    cost = models.IntegerField(default=0)
    description = RichTextField()
    hot = models.BooleanField()
    new = models.BooleanField()
    most_sellable = models.BooleanField()
    feature_image_url = models.CharField(max_length=250)
    products = models.ManyToManyField(Product)


# sales app
class Invoice(models.Model):
    user = models.ForeignKey(User, related_name="User", null=False, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField()
    discount = models.IntegerField()
    created_by = models.ForeignKey(User, related_name="Created_By",on_delete=models.CASCADE)
    created_at = models.DateTimeField('Draft date', auto_now_add=True)
    updated_at = models.DateTimeField('Draft date', auto_now=True)


class Payment(models.Model):
    PAYMENT_FULL = "FL"
    PAYMENT_PARTIAL = "PL"
    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_FULL, "Partial"),
        (PAYMENT_PARTIAL, "Full"),
    )

    INITIATED = "IN"
    PROCESSED = "PR"
    REJECTED = "RJ"
    PAYMENT_STATUS_CHOICES = [
        (INITIATED, "Initiated"),
        (PROCESSED, "Processed"),
        (REJECTED, "Rejected")
    ]
    Invoice = models.ForeignKey(Invoice, null=False, on_delete=models.CASCADE)
    payment_link = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_FULL)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default=INITIATED, max_length=2)
    