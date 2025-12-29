from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from reports.models import Report
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "home/product_list.html"
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "marketing/product_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["reports"] = Report.objects.filter(product=kwargs.get('object'))
        return context

class DashboardProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "home/dashboard_product.html"
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
