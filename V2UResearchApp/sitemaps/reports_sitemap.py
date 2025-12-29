from django.contrib.sitemaps import Sitemap 
from reports.models import Report
from datetime import datetime

class ReportsSitemap(Sitemap):
    def items(self):
        return Report.objects.filter(published_date__lte=datetime.now()).order_by('-published_date')
    def lastmod(self, obj):
        return obj.published_date
