from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Report
from marketing.models import Product
from users.models import User, Region
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from .mixins import ProductPermissionRequiredMixin
from company.models import ResearchTypes
from home.mixins import EssentialsMixin
from datetime import datetime

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

import logging

logger = logging.getLogger(__name__)
# Create your views here.

class ReportListView(EssentialsMixin, LoginRequiredMixin, ListView):
    model = Report
    template_name = "home/dashboard_report.html"
    paginate_by = 12  # Show 12 reports per page for better grid layout

    def get_queryset(self):
        """Get filtered and sorted queryset based on user permissions and filters"""
        # Get user permissions
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(
            content_type__app_label=app_lbl, 
            content_type__model=model_name
        )
        
        # Extract product names from permissions
        accessible_product_names = []
        for permission in permissions:
            if permission.codename.find("can_view_") == 0 and self.request.user.has_perm('users.' + permission.codename):
                accessible_product_names.append(permission.name.replace('Can View ', ''))
        
        # Get region from context (set by EssentialsMixin)
        region = self.request.COOKIES.get('region')
        region_obj = None
        if region:
            try:
                region_obj = Region.objects.get(country_code=region)
            except:
                region_obj = Region.objects.filter(is_default=True).first()
        else:
            region_obj = Region.objects.filter(is_default=True).first()
        
        # Base queryset - reports user has access to
        if region_obj and accessible_product_names:
            accessible_products = Product.objects.filter(name__in=accessible_product_names, regions=region_obj)
            queryset = Report.objects.filter(
                product__in=accessible_products,
                region=region_obj,
                published_date__lte=datetime.now()
            ).distinct()
        else:
            queryset = Report.objects.none()
        
        # Apply search filter
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                short_description__icontains=search_query
            ) | queryset.filter(
                segment__name__icontains=search_query
            )
        
        # Apply product filter
        product_id = self.request.GET.get('product', '').strip()
        if product_id:
            try:
                queryset = queryset.filter(product__id=int(product_id))
            except (ValueError, TypeError):
                pass
        
        # Apply sector filter
        sector_id = self.request.GET.get('sector', '').strip()
        if sector_id:
            try:
                queryset = queryset.filter(sector__id=int(sector_id))
            except (ValueError, TypeError):
                pass
        
        # Apply date range filter
        date_range = self.request.GET.get('date_range', '').strip()
        if date_range:
            from datetime import timedelta
            today = timezone.now()
            if date_range == '7':
                queryset = queryset.filter(published_date__gte=today - timedelta(days=7))
            elif date_range == '30':
                queryset = queryset.filter(published_date__gte=today - timedelta(days=30))
            elif date_range == '90':
                queryset = queryset.filter(published_date__gte=today - timedelta(days=90))
        
        # Apply sorting
        sort_by = self.request.GET.get('sort', 'newest').strip()
        if sort_by == 'oldest':
            queryset = queryset.order_by('published_date')
        elif sort_by == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort_by == 'title_desc':
            queryset = queryset.order_by('-title')
        else:  # Default: newest
            queryset = queryset.order_by('-published_date')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user permissions for statistics
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(
            content_type__app_label=app_lbl, 
            content_type__model=model_name
        )
        
        # Extract accessible product names
        accessible_product_names = []
        for permission in permissions:
            if permission.codename.find("can_view_") == 0 and self.request.user.has_perm('users.' + permission.codename):
                accessible_product_names.append(permission.name.replace('Can View ', ''))
        
        # Get region
        region = context.get('region')
        
        # Calculate statistics
        if region and accessible_product_names:
            accessible_products = Product.objects.filter(name__in=accessible_product_names, regions=region)
            
            # Total reports count
            total_reports = Report.objects.filter(
                product__in=accessible_products,
                region=region,
                published_date__lte=datetime.now()
            ).distinct().count()
            
            # Recent reports (last 30 days)
            from datetime import timedelta
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_reports = Report.objects.filter(
                product__in=accessible_products,
                region=region,
                published_date__gte=thirty_days_ago,
                published_date__lte=datetime.now()
            ).distinct().count()
            
            context['total_reports_count'] = total_reports
            context['recent_reports_count'] = recent_reports
            context['accessible_products'] = accessible_products
            context['accessible_products_count'] = accessible_products.count()
        else:
            context['total_reports_count'] = 0
            context['recent_reports_count'] = 0
            context['accessible_products'] = []
            context['accessible_products_count'] = 0
        
        # Get all sectors for filter dropdown
        from company.models import Sector
        context['all_sectors'] = Sector.objects.all().order_by('sector_name')
        
        # Current filter values
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_product'] = self.request.GET.get('product', '')
        context['selected_sector'] = self.request.GET.get('sector', '')
        context['selected_date_range'] = self.request.GET.get('date_range', '')
        context['selected_sort'] = self.request.GET.get('sort', 'newest')
        
        # Check if any filters are applied
        context['has_filters'] = bool(
            context['search_query'] or 
            context['selected_product'] or 
            context['selected_sector'] or 
            context['selected_date_range']
        )
        
        # Rename object_list to reports for template compatibility
        context['reports'] = context['object_list']
        
        return context

from home.forms import LeadForm

class ReportDetailView(EssentialsMixin, ProductPermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Report
    template_name = "report/report_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Region is already handled by EssentialsMixin safe refactor
        
        # Add Lead Form for bottom of page
        report_title = self.object.title if self.object else "Report"
        context['form'] = LeadForm(initial={'source': f"Report Page: {report_title}"})
        
        return context
    
class FreeReportDetailView(EssentialsMixin, DetailView):
    model = Report
    template_name = "report/report_detail.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return context

class FreeReportListView(EssentialsMixin, ListView):
    model = Report
    template_name = "home/free_reports.html"
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # EssentialsMixin handles context['reports'] for daily/featured, but this view needs specific free reports
        # Wait, the original code overwrote 'reports'.
        region = context.get('region')
        if region:
             reports = Report.objects.filter(is_free=True, region=region, published_date__lte=datetime.now()).order_by('-published_date')
        else:
             reports = []
             
        context["reports"] = reports
        return context

class DailyReportListView(EssentialsMixin, ListView):
    model = Report
    template_name = "home/daily_reports.html"
    paginate_by = 21

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            app_lbl = User._meta.app_label
            model_name = User._meta.model_name
            permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)
        else:
            permissions = []
            
        reports = []
        context["perm"] = permissions
        
        if self.request.user.is_authenticated:
            for permission in permissions:
                if permission.codename.find("can_view_")==0 and self.request.user.has_perm('users.'+permission.codename):
                    reports.append(permission.name.replace('Can View ', ''))
        
        products = Product.objects.filter()
        segments = ResearchTypes.objects.all()
        segment = None
        region = context.get('region')
        
        reports_qs = Report.objects.none()
        
        if region:
            if 'slug' in self.kwargs and self.kwargs['slug']!='':
                slug = self.kwargs['slug']
                try:
                    rst = ResearchTypes.objects.get(slug=slug)
                    segment = rst
                    reports_qs = Report.objects.filter(product__in=products, is_daily=True, segment=rst, region=region, published_date__lte=datetime.now()).order_by('-published_date')
                except:
                    pass
            else:
                reports_qs = Report.objects.filter(product__in=products, is_daily=True, region=region, published_date__lte=datetime.now()).order_by('-published_date')
        
        paginator = Paginator(reports_qs, self.paginate_by)
        page = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page)

        try:
            page_reports = paginator.page(page)
        except PageNotAnInteger:
            page_reports = paginator.page(1)
        except EmptyPage:
            page_reports = paginator.page(paginator.num_pages)

        context["segments"] = segments
        context["segment"] = segment
        context["reports"] = page_reports
        
        return context

class SearchReportList(EssentialsMixin, ListView):
    model = Report
    template_name = "report/search_report.html"
    paginate_by = 10
    
    def get_queryset(self):
        self.query = self.request.GET.get("query", "90000")
        object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_results'] = self.model.objects.filter(title__icontains=self.query)
        return context