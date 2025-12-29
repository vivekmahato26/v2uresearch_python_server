from django.contrib.sitemaps import Sitemap 
from marketing.models import Product
from reports.models import Report
# from company.models import Sector
from home.models import Pages
from datetime import datetime

class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.filter(is_active=True)
    def lastmod(self, obj):
        return datetime.now()

class ReportSitemap(Sitemap):
    def items(self):
        return Report.objects.filter(published_date__lte=datetime.now()).order_by('-published_date')
    def lastmod(self, obj):
        return obj.published_date


class PagesSitemap(Sitemap):
    def items(self):
        return Pages.objects.filter()
    def lastmod(self, obj):
        return datetime.now()