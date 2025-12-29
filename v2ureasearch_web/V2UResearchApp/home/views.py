from typing import Any, Dict
from django import http
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Region
from company.models import Sector

from django.urls import reverse
from django.http import HttpResponse
from marketing.models import Product, Lead
from .models import Pages
from reports.models import Report

from django.views.generic.edit import CreateView
from django.views.generic import DetailView
# Create your views here.


def setregioncookie():  
    response = HttpResponse("Cookie Set")
    response.set_cookie('region', 'USA')
    return response  
def getregioncookie(request):  
    region  = request.COOKIES['region']  
    return HttpResponse("region @: "+  region);  


class HomeView(TemplateView):
    template_name = "home/index.html"

    def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('region', 'USA')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # try:
        #     region = Region.objects.filter(country_code=self.request.COOKIES['region'])
        #     if region:
        #         region = region[0]
        # except:
        #     region = Region.objects.get(is_default=1)
        region = Region.objects.get(is_default=1)
        context['region'] = region
        context['regions'] = Region.objects.filter()
        context['products'] = Product.objects.filter(is_active=True, region=region)
        context['reports'] = Report.objects.filter(region=region)[:4]
        context['featured_reports'] = Report.objects.filter(region=region).order_by('-published_date')[:4]
        # context['featured_reports'] = Report.objects.filter(is_featured=True)[:4]
        context['sectors'] = Sector.objects.all()[:4]
        return context


class ContactUsView(CreateView):
    template_name = "home/contact_us.html"
    model = Lead
    fields = ["first_name", "last_name", "email", "phone"]

    def get_success_url(self):
        return reverse('success_page')


class SuccessView(TemplateView):
    template_name = "home/success.html"


class PagesView(DetailView):
    model = Pages
    template_name = "home/pages_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context


# class DashboardProductView(LoginRequiredMixin, TemplateView):
#     template_name = "home/dashboard_product.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.filter(is_active=True)[:4]
#         context['reports'] = Report.objects.all()[:4]
#         context['featured_reports'] = Report.objects.filter(is_featured=True)[:4]
#         context['sectors'] = Sector.objects.all()[:4]
#         return context


# class DashboardReportView(LoginRequiredMixin, TemplateView):
#     template_name = "home/dashboard_report.html"
