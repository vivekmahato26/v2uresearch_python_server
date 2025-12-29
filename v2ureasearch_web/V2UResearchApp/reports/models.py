from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from users.models import Region
from marketing.models import Product
from company.models import Sector, ResearchTypes, Company
from django.contrib.auth.models import User 

# Create your models here.


class Report(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    short_description = models.CharField(max_length=255)
    description = RichTextField()
    product = models.ManyToManyField(Product, null=False, )
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    draft_date = models.DateTimeField('Draft date', auto_now=True)
    region = models.ManyToManyField(Region, null=False)
    # recommendation = 
    traget_price = models.IntegerField()
    segment = models.ForeignKey(ResearchTypes, null=True, on_delete=models.CASCADE)
    sector = models.ManyToManyField(Sector, null=False)
    company = models.ManyToManyField(Company, null=False)
    is_free = models.BooleanField(null=True)
    is_featured = models.BooleanField(null=True)
    feature_image_url = models.CharField(max_length=250)


    class Meta:
        verbose_name_plural = "Reports"
        verbose_name = "Report"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('report-detail', args=(str(self.slug),))
