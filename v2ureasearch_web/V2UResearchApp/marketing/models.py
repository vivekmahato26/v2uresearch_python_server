from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from users.models import Region
from django.db.models import JSONField

# marketing app
class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    source =  models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    phone = PhoneNumberField()
    user_agent = JSONField()
    # created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Draft date', auto_now_add=True)
    updated_at = models.DateTimeField('Draft date', auto_now=True)

    class Meta:
        verbose_name_plural = "Leads"
        verbose_name = "Lead"
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    duration = models.CharField(max_length=200)
    cost = models.IntegerField(default=0)
    description = models.TextField()
    hot = models.BooleanField()
    new = models.BooleanField()
    most_sellable = models.BooleanField()
    feature_image_url = models.CharField(max_length=250)
    is_active = models.BooleanField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.slug)])
    