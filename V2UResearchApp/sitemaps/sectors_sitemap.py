from django.contrib.sitemaps import Sitemap 
from company.models import Sector
from datetime import datetime

class SectorsSitemap(Sitemap):
    def items(self):
        return Sector.objects.filter()
    def lastmod(self, obj):
        return datetime.now()
