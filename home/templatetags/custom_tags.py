from django import template
register = template.Library()

from company.models import Sector
from home.models import Pages
from users.models import Region

from django.db.models import Count, Q

@register.simple_tag
def sectors(region):
    if not region or isinstance(region, str):
        return Sector.objects.none()
    
    # Filter sectors that have at least one report in the current region
    return Sector.objects.filter(regions=region) \
        .annotate(num_reports=Count('report', filter=Q(report__region=region))) \
        .filter(num_reports__gt=0) \
        .order_by().exclude(sector_name__in=["","N/A"])

@register.simple_tag
def pages(region):
    if not region or isinstance(region, str):
        return Pages.objects.none()
    return Pages.objects.filter(region=region)

@register.simple_tag
def regions():
    return Region.objects.filter(is_active=True)

@register.filter(name="index")
def index(indexable, i):
    try:
        return indexable[i]
    except:
        return 'Hello'

from django.conf import settings

@register.filter(name="replace_media_url")
def replace_media_url(value):
    """
    Replaces /media/ path with actual MEDIA_URL from settings.
    Useful for Rich Text fields where paths are hardcoded relative to domain.
    """
    if isinstance(value, str):
        # We replace the relative path /media/ with the absolute S3 URL
        # e.g. /media/uploads/ -> https://bucket.s3.../media/uploads/
        return value.replace('/media/', settings.MEDIA_URL)
    return value