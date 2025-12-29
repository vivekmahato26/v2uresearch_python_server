from django.db import models
from django.urls import reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from users.models import Region

class Pages(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    feature_image_url = models.ImageField(upload_to='uploads/pages/%Y/%m/%d/')
    description = RichTextUploadingField()
    meta_keyword = models.CharField(max_length=255)
    summary = RichTextUploadingField()
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Pages"
        verbose_name = "Page"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pages', args=[str(self.slug)])

class Blocks(models.Model):
    block_name = models.CharField(max_length=50)
    content = RichTextUploadingField()
    region = models.ForeignKey(Region, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Blocks"
        verbose_name = "Block"
    
    def __str__(self):
        return self.block_name