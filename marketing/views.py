from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from reports.mixins import ProductPermissionRequiredMixin
from users.models import Region, User

from reports.models import Report
from .models import Product, Articles, Lead
from django.contrib.auth.mixins import LoginRequiredMixin
from csv_export.views import CSVExportView
from home.mixins import EssentialsMixin

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from datetime import datetime
from home.forms import LeadForm


import logging

logger = logging.getLogger(__name__)

class LeadExportView(LoginRequiredMixin, CSVExportView):
    model = Lead
    fields = "__all__"
    ordering = ["-created_at"]

    def get_filename(self, queryset):
        return "data-export-{!s}.csv".format(timezone.now())
    


# Create your views here.

class ProductListView(EssentialsMixin, ListView):
    model = Product
    template_name = "home/product_list.html"
    paginate_by = 30  # if pagination is desired
    queryset = Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)
        reports_perms = []
        context["perm"] = permissions
        for permission in permissions:
            if permission.codename.find("can_view_")==0 and self.request.user.has_perm('users.'+permission.codename):
                reports_perms.append(permission.name.replace('Can View ', ''))

        # region = Region.objects.get(is_default=1)
        region = context['region']
        # context['region'] = region
        # context['region'] = region
        context['products'] = Product.objects.filter(is_active=True, regions=region)
        context["perms"] = list(map(lambda x: True if x.name in reports_perms else False, context['products']))
        context['reports'] = Report.objects.filter(region=region, published_date__lte=datetime.now())[:4]
        # context['featured_reports'] = Report.objects.filter(regions=region).order_by('-published_date')[:4]
        context["now"] = timezone.now()
        return context

class ProductDetailView(EssentialsMixin, DetailView):
    model = Product
    template_name = "marketing/product_detail.html"
    paginate_by = 30

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)
        reports_perms = []
        context["perm"] = permissions
        for permission in permissions:
            if permission.codename.find("can_view_")==0 and self.request.user.has_perm('users.'+permission.codename):
                reports_perms.append(permission.name.replace('Can View ', ''))

        # region = Region.objects.get(is_default=1)
        region = context['region']
        # context['region'] = region
        # context['region'] = region
        context['products'] = Product.objects.filter(is_active=True, regions=region)
        context["purchased"] = kwargs.get('object').name in reports_perms
        lst_reports = Report.objects.filter(product=kwargs.get('object'), region=region, published_date__lte=datetime.now()).order_by("-published_date")
        paginator = Paginator(lst_reports, self.paginate_by)

        page = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page)

        try:
            page_reports = paginator.page(page)
        except PageNotAnInteger:
            page_reports = paginator.page(1)
        except EmptyPage:
            page_reports = paginator.page(paginator.num_pages)

        context["reports"] = page_reports
        context['form'] = LeadForm(initial={'source': f"Product: {kwargs.get('object').name}"})

        return context

class DashboardProductListView(EssentialsMixin, LoginRequiredMixin, ListView):
    model = Product
    template_name = "home/dashboard_product.html"
    paginate_by = 100  # if pagination is desired
    # queryset = Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)
        reports_perms = []
        context["perm"] = permissions
        for permission in permissions:
            if permission.codename.find("can_view_")==0 and self.request.user.has_perm('users.'+permission.codename):
                reports_perms.append(permission.name.replace('Can View ', ''))

        context["now"] = timezone.now()
        # region = Region.objects.get(is_default=1)
        region = context['region']
        
        # context['region'] = region
        # context['region'] = region
        context['products'] = Product.objects.filter(regions=region, is_active=True)
        logger.error(context['products'].values_list('id', 'name'))
        context["perms"] = list(map(lambda x: True if x.name in reports_perms else False, context['products']))
        context["reports"] = Report.objects.filter(product=kwargs.get('object'), region=region, published_date__lte=datetime.now())
        return context

class ArticlesListView(EssentialsMixin, ListView):
    model = Articles
    template_name = "articles/list.html"
    paginate_by = 100  # if pagination is desired
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        region = context['region']
        # context['regions'] = Region.objects.all(is_active=True)
        # context['products'] = Product.objects.filter(is_active=True, region=region)
        # context['reports'] = Report.objects.filter(region=region)[:4]
        # context['featured_reports'] = Report.objects.filter(region=region, published_date__lte=datetime.now()).order_by('-published_date')[:4]
        # context["now"] = timezone.now()
        return context

class ArticlesDetailView(EssentialsMixin, DetailView):
    model = Articles
    template_name = "articles/details.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        region = context['region']
        # context['regions'] = Region.objects.filter()
        context['products'] = Product.objects.filter(is_active=True, regions=region)
        context['article'] = Articles.objects.get(slug=kwargs.get('object').slug)
        return context

