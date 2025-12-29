from django.contrib.sitemaps import Sitemap 
from marketing.models import Articles

class ArticlesSitemap(Sitemap):
    def items(self):
        return Articles.objects.filter().order_by('-published_date')
    def lastmod(self, obj):
        return obj.published_date
