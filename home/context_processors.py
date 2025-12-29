from users.models import Region
from marketing.models import Product, SocialHandle
from company.models import Sector
from home.models import Blocks, Pages
from datetime import datetime


def footer_context(request):
    """
    Context processor to inject footer-related data globally.
    This ensures the footer renders correctly on all pages, including auth pages.
    """
    # 1. Determine Region String from Cookie, Host, or Default
    region_str = request.COOKIES.get('region', None)
    
    # Hostname determination
    try:
        region_hn = request.get_host()
        current_site = Region.objects.filter(region_hostname__contains=region_hn).first()
        if current_site:
            hostname_region_str = current_site.country_code
        else:
            hostname_region_str = None
    except:
        hostname_region_str = None

    if not region_str and hostname_region_str:
        region_str = hostname_region_str
        
    if region_str:
        region_str = str.upper(region_str)

    # 2. Fetch Region Object
    region = None
    if region_str:
        region = Region.objects.filter(country_code=region_str).first()
    
    if not region:
        region = Region.objects.filter(is_default=True).first()
        
    if not region:
        region = Region.objects.filter(is_active=True).first()
    
    # 3. Populate Context
    context = {}
    
    if region:
        context['region'] = region
        context['sectors'] = Sector.objects.filter(regions=region)
        context['products'] = Product.objects.filter(is_active=True, regions=region)
        context['social_handles'] = SocialHandle.objects.all()
        
        try:
            block = Blocks.objects.filter(region=region, block_name='Disclaimer').first()
            context['disclaimer'] = block.content if block else ''
        except:
            context['disclaimer'] = ''
    else:
        context['region'] = None
        context['sectors'] = Sector.objects.none()
        context['products'] = Product.objects.none()
        context['social_handles'] = SocialHandle.objects.none()
        context['disclaimer'] = ''
    
    context['regions'] = Region.objects.filter(is_active=True)
    
    return context
