from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from users.models import User, Region
from marketing.models import Product, SocialHandle
from reports.models import Report
from company.models import Sector
from datetime import datetime
from home.models import Blocks, Pages
import os


from django.db.models import Count, Q

class EssentialsMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Determine Region String from Cookie, Host, or Default
        region_str = self.request.COOKIES.get('region', None)
        
        # Hostname determination
        try:
            region_hn = self.request.get_host()
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
            
        print(f"DEBUG: EssentialsMixin resolved region_str: {region_str}")

        # 2. Fetch Region Object
        region = None
        if region_str:
            region = Region.objects.filter(country_code=region_str).first()
        
        if not region:
            region = Region.objects.filter(is_default=True).first()
            
        if not region:
            region = Region.objects.filter(is_active=True).first()
            
        # 3. Populate Context
        if region:
            context['region'] = region
            # Filter sectors that have at least one report in the current region
            context['sectors'] = Sector.objects.filter(regions=region) \
                .annotate(num_reports=Count('report', filter=Q(report__region=region))) \
                .filter(num_reports__gt=0).order_by('-priority', 'sector_name')
            
            # Use filter() instead of get() to be safe, though ID error suggests bad object passed
            context['products'] = Product.objects\
                .filter(is_active=True, regions=region)\
                .only('name', 'slug', 'hot', 'new',
                        'most_sellable', 'is_platinum',
                        'is_active', 'regions')
            
            context['reports'] = Report.objects\
                .filter(region=region, is_daily=True, published_date__lte=datetime.now())\
                .only('title', 'slug', 'short_description')\
                .order_by('-published_date')[:6]
    
            context['featured_reports'] = Report.objects\
                .filter(region=region, is_daily=False)\
                .only('title', 'slug', 'short_description')\
                .order_by('-published_date')[:4]
            
            try:
                about_page = Pages.objects.filter(title__icontains="about", region=region).first()
                if about_page:
                    context["About_Page"] = about_page.slug
                else:
                    context["About_Page"] = 'about'
            except:
                context["About_Page"] = 'about'
            
            try:
                block = Blocks.objects.filter(region=region, block_name='Disclaimer').first()
                if block:
                    context['disclaimer'] = block.content
                else:
                    context['disclaimer'] = ''
            except:
                context['disclaimer'] = ''
        else:
            # Fallback if NO region exists in DB at all
            context['region'] = None
            context['sectors'] = Sector.objects.none()
            context['products'] = Product.objects.none()
            context['reports'] = Report.objects.none()
            context['featured_reports'] = Report.objects.none()
            context['disclaimer'] = ''

        context["hostname"] = self.request.get_host()
        context['regions'] = Region.objects.filter(is_active=True)
        context['social_handles'] = SocialHandle.objects.all()

        return context