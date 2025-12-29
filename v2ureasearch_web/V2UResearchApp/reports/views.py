from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Report
from marketing.models import Product
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from .mixins import ProductPermissionRequiredMixin


# Create your views here.

class ReportListView(ListView):
    model = Report
    template_name = "home/dashboard_report.html"
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_lbl = User._meta.app_label
        model_name = User._meta.model_name
        permissions = self.request.user.user_permissions.filter(content_type__app_label=app_lbl, content_type__model=model_name)

        context["perm"] = permissions
        # for :
        reports = ""
        if self.request.user.has_perm('users.can_view_us_coffee'):
            product = Product.objects.get(name="US Coffee")
            reports = Report.objects.filter(product=product)
        if self.request.user.has_perm('users.can_view_au_coffee'):
            product = Product.objects.get(name="AU Coffee")
            reports = Report.objects.filter(product=product)
        if self.request.user.has_perm('users.can_view_us_little_champ'):
            product = Product.objects.get(name="US Little Champ")
            reports = Report.objects.filter(product=product)
        if self.request.user.has_perm('users.can_view_au_little_champ'):
            product = Product.objects.get(name="AU Little Champ")
            reports = Report.objects.filter(product=product)
        
        context["reports"] = reports
        return context

class ReportDetailView(LoginRequiredMixin, ProductPermissionRequiredMixin, DetailView):
    model = Report
    template_name = "report/report_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context