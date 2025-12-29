from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from users.models import Region

class Pages(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    feature_image_url = models.CharField(max_length=250)
    description = RichTextField()
    meta_keyword = models.CharField(max_length=255)
    summary = RichTextField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Pages"
        verbose_name = "Page"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pages', args=[str(self.slug)])
