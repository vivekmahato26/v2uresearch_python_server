from django.shortcuts import render
from users.models import Region
from company.models import Sector
from marketing.models import Product, SocialHandle
from home.models import Blocks, Pages
from home.forms import LeadForm

class ProductPermissionRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        product=getattr(self.get_object(), 'product').all()
        perms = ["Can View "+p.name for p in product]
        
        permissions = self.request.user.user_permissions.filter(name__in=perms)

        context = {"report": self.get_object()}

        if permissions:
            return super().dispatch(request, *args, **kwargs)
        else:
            # 1. Fetch Region (Simplified logic from EssentialsMixin)
            region_str = request.COOKIES.get('region', None)
            if not region_str:
                 # Hostname fallback
                try:
                    region_hn = request.get_host()
                    current_site = Region.objects.filter(region_hostname__contains=region_hn).first()
                    if current_site:
                        region_str = current_site.country_code
                except:
                    pass
            
            region = None
            if region_str:
                region = Region.objects.filter(country_code=str.upper(region_str)).first()
            if not region:
                region = Region.objects.filter(is_default=True).first()
            if not region:
                region = Region.objects.filter(is_active=True).first()

            # 2. Populate Footer Context
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
                 context['disclaimer'] = ''

            # Add Lead Form for unsubscribed view
            report_title = self.get_object().title
            context['form'] = LeadForm(initial={'source': f"Unsubscribed Report Page: {report_title}"})
            return render(request, "home/unsubscribed_report.html", context)