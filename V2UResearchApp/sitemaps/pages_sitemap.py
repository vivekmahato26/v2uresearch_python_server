from django.contrib.sitemaps import Sitemap 
from home.models import Pages
from datetime import datetime

class PagesSitemap(Sitemap):
    def items(self):
        return Pages.objects.filter()
    def lastmod(self, obj):
        return datetime.now()