from django import template
register = template.Library()

from company.models import Sector
from home.models import Pages
from users.models import Region

@register.simple_tag
def sectors():
    return Sector.objects.order_by().exclude(sector_name__in=["","N/A"])

@register.simple_tag
def pages():
    return Pages.objects.all()

@register.simple_tag
def regions():
    return Region.objects.all()