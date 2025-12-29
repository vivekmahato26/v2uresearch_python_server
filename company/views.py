from django.shortcuts import render
from django.views.generic import DetailView

from reports.models import Report
from .models import Sector
from users.models import Region, User
from marketing.models import Product  
from home.mixins import EssentialsMixin 
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class SectorDetailView(EssentialsMixin, DetailView):
    model = Sector
    template_name = "company/sector_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)
        reports = []
        # context["perm"] = permissions
        
        for permission in permissions:
            if permission.codename.find("can_view_")==0 and self.request.user.has_perm('users.'+permission.codename):
                reports.append(permission.name.replace('Can View ', ''))
        context['perms'] = ','.join(reports)
        # region = Region.objects.get(is_default=1)
        region = context['region']
        # context['region'] = region
        context["reports"] = Report.objects.filter(sector=kwargs.get('object'), region=region, published_date__lte=datetime.now()).order_by('-published_date')
        # context['regions'] = Region.objects.filter()
        context['products'] = Product.objects.filter(is_active=True, regions=region)
        return context

from django.views.generic import ListView
from django.db.models import Count, Q

class SectorListView(EssentialsMixin, ListView):
    model = Sector
    template_name = "company/sector_list.html"
    context_object_name = 'sectors'
    
    def get_queryset(self):
        region = self.request.COOKIES.get('region')
        if region:
            try:
                region_obj = Region.objects.get(country_code=region)
                # Helper logic similar to mixin but specific for this list
                return Sector.objects.filter(regions=region_obj) \
                    .annotate(num_reports=Count('report', filter=Q(report__region=region_obj))) \
                    .filter(num_reports__gt=0).order_by('-priority', 'sector_name')
            except:
                pass
        
        # Fallback
        return Sector.objects.all().order_by('-priority', 'sector_name')
