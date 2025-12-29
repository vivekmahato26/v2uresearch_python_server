from django.db import models
from django.urls import reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from users.models import Region
from marketing.models import Product
from company.models import Sector, ResearchTypes, Company
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    class TemplatesChoices(models.TextChoices):
        T1 = 't20231201', _('Template Dec 23')
        T2 = 't20241001', _('Template Oct 24')

    class RiskLevelChoices(models.TextChoices):
        LOW = 'low', _('Low')
        MED = 'med', _('Medium')
        HIGH = 'hig', _('High')
        NONE = 'NA', _('None')

    class RecommendationChoices(models.TextChoices):
        BUY = 'BU', _('Buy')
        SPECULATIVEBUY = 'SB', _('Speculative Buy')
        HOLD = 'HD', _('Hold')
        SELL = 'SL', _('Sell')
        EXPENSIVE = 'EP', _('Expensive')
        WAITNWATCH = 'WW', _('Wait & Watch')
        UPDATE = 'UP', _('Update')
        NONE = 'NA', _('None')

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    short_description = models.CharField(max_length=255)
    custom_templates = models.CharField(max_length=9, 
                        choices=TemplatesChoices.choices, 
                        default=TemplatesChoices.T2)
    summary_title = models.CharField(max_length=255, null=True)
    description = RichTextUploadingField()
    left_description = RichTextUploadingField()
    product = models.ManyToManyField(Product, null=False, )
    # product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="author", name="author" )
    published_date = models.DateTimeField()
    draft_date = models.DateTimeField('Draft date', auto_now=True)
    region = models.ManyToManyField(Region, null=False)
    # recommendation = 
    # traget_price = models.IntegerField()
    traget_price = models.FloatField(default=0.00)
    cmp = models.FloatField(default=0.00)
    risk_level = models.CharField(null=True, max_length=3,                    
                    choices=RiskLevelChoices.choices, 
                    default=RiskLevelChoices.NONE)
    recommendation = models.CharField(null=True, max_length=2,
                        choices=RecommendationChoices.choices, 
                        default=RecommendationChoices.NONE)
    segment = models.ForeignKey(ResearchTypes, null=True, on_delete=models.CASCADE)
    sector = models.ManyToManyField(Sector, null=False)
    company = models.ManyToManyField(Company, null=False)
    is_free = models.BooleanField(null=True)
    is_featured = models.BooleanField(null=True)
    is_daily = models.BooleanField(null=True)
    feature_image_url = models.ImageField(upload_to='uploads/reports/%Y/%m/%d/', null=True)
    pdf_url = models.FileField(upload_to='uploads/reports/%Y/%m/%d/', null=True)

    class Meta:
        verbose_name_plural = "Reports"
        verbose_name = "Report"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('report-detail', args=(str(self.slug),))

    def get_free_absolute_url(self):
        return reverse('free-report-detail', args=(str(self.slug),))
