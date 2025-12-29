from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from users.models import Region
from django.db.models import JSONField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


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
    setup_password = models.CharField(max_length=15, null=False, default='Welcome@v2u')
    is_free_trial = models.BooleanField(null=False, default=False)
    first_time = models.BooleanField(null=False, default=True)

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
    # description = models.TextField()
    description = RichTextUploadingField()
    hot = models.BooleanField()
    new = models.BooleanField()
    most_sellable = models.BooleanField()
    is_platinum = models.BooleanField(default=False)
    # feature_image_url = models.CharField(max_length=250)
    feature_image_url = models.ImageField(upload_to='uploads/products/')
    is_active = models.BooleanField()
    # region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE, related_name="pregion")
    regions = models.ManyToManyField(Region, null=False, related_name="pregions")
    spec_1 = models.CharField(max_length=255, default="Specification", null=False)
    spec_2 = models.CharField(max_length=255, default="Specification", null=False)
    spec_3 = models.CharField(max_length=255, default="Specification", null=False)
    spec_4 = models.CharField(max_length=255, default="Specification", null=False)
    spec_5 = models.CharField(max_length=255, default="Specification", null=False)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.slug)])
    
    def save(self, **kwargs):
        super().save(**kwargs)
        print(kwargs)
        # adding permissions for this product
        content_type = ContentType.objects.get(id=14)

        perm_name = self.name
        perm_codename = perm_name.lower()
        perm_codename = perm_codename.replace(" ", "_")
        permission = Permission.objects.update_or_create(
            codename=f'can_{perm_codename}',
            name=f'Can View {perm_name}',
            content_type=content_type
        )
    
class Articles(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    short_description = models.CharField(max_length=255)
    description = RichTextUploadingField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    draft_date = models.DateTimeField('Draft date', auto_now=True)
    region = models.ManyToManyField(Region, null=False)
    # recommendation = 
    # traget_price = models.IntegerField()
    feature_image_url = models.ImageField(upload_to='uploads/articles/%Y/%m/%d/')

    class Meta:
        verbose_name_plural = "Articles"
        verbose_name = "Article"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article', args=(str(self.slug),))

class SocialHandle(models.Model):
    handle_choices = (
        ('fb', 'FACEBOOK'),
        ('x', 'X'),
        ('li', 'LINKEDIN'),
        ('insta', 'INSTAGRAM'),
        ('yt', 'YOUTUBE')
    )
    name = models.CharField(null=False, max_length=50)
    handle = models.CharField(null=False, max_length=10, choices=handle_choices)
    region = models.ManyToManyField(Region, null=False)
    handle_url = models.CharField(max_length=255, null=False, default='#')

    def __str__(self):
        return f"{self.name} {self.handle}"
