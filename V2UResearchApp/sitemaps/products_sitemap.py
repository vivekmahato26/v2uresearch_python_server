from django.contrib.sitemaps import Sitemap 
from marketing.models import Product
from datetime import datetime

class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(is_active=True)
    def lastmod(self, obj):
        return datetime.now()
