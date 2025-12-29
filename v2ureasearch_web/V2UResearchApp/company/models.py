from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from users.models import Region

# Create your models here.

class Sector(models.Model):
    sector_name = models.CharField(max_length=200)
    slug = models.SlugField()
    feature_image_url = models.CharField(max_length=200)
    description = RichTextField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Sectors"
        verbose_name = "Sector"
    
    def __str__(self):
        return self.sector_name
    
    def get_absolute_url(self):
        return reverse('sector-detail', args=[str(self.slug)])


class ResearchTypes(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Research Types"
        verbose_name = "Research Type"
    
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200)
    sector = models.ManyToManyField(Sector, null=False, )
    symbol = models.CharField(max_length=200)
    description = RichTextField()
    slug = models.SlugField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"
    
    def __str__(self):
        return self.name

