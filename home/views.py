from typing import Any, Dict
from django import http
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Region
from company.models import Sector

from django.urls import reverse
from django.http import HttpResponse
from marketing.models import Product, Lead
from .models import Pages
from reports.models import Report
from testimonials.models import ClientTestimonials

from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .mixins import EssentialsMixin
from home.models import Blocks

def setregioncookie():  
    response = HttpResponse("Cookie Set")
    response.set_cookie('region', 'USA')
    return response

def getregioncookie(request):  
    region  = request.COOKIES['region']  
    return HttpResponse("region @: "+  region);  

def switchCountry(request, to):
    # Normalize the input to uppercase
    region_code = to.upper()
    
    # Determine the target domain
    if region_code == 'AUS':
        target_domain = 'https://v2uresearch.com.au'
    else:
        target_domain = 'https://v2uresearch.com'
    
    # Create the redirect response to the target domain's home page
    response = redirect(target_domain + '/')
    
    # Set the cookie so the site remembers the preference across domains
    # Note: For cookies to work across .com and .com.au, 
    # the browser will treat them as separate cookies per domain.
    response.set_cookie('region', region_code, max_age=60*60*24*365)
    
    return response

class SwitchView(EssentialsMixin, TemplateView):
    template_name = 'home/switch_countries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AboutUsView(EssentialsMixin, TemplateView):
    template_name = "home/about_us.html"

    
class HomeView(EssentialsMixin, TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['testimonials'] = ClientTestimonials.objects.filter(region=context['region']).order_by('-id')[:5]
        try:
            block = Blocks.objects.get(region=context['region'], block_name='Home About')
            context["AboutBlock"] = block.content
        except:
            context["AboutBlock"] = f"<h2>About {context['region']}</h2>"
        
        return context


from home.forms import LeadForm

from django.contrib import messages

class ContactUsView(EssentialsMixin, CreateView):
    template_name = "home/contact_us.html"
    form_class = LeadForm
    
    def get_initial(self):
        initial = super().get_initial()
        initial['source'] = "Contact Us Page"
        return initial
    # model = Lead # Removed as form_class defines model
    # fields = ... # Removed as form_class defines fields

    def form_valid(self, form):
        # Capture User Agent
        user_agent_str = self.request.META.get('HTTP_USER_AGENT', 'Unknown')
        form.instance.user_agent = {"browser": user_agent_str}
        
        # Save and add success message
        response = super().form_valid(form)
        messages.success(self.request, "Thank you! Your inquiry has been submitted successfully. We will contact you soon.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the form details below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('success_page')


class SuccessView(EssentialsMixin, TemplateView):
    template_name = "home/success.html"


class PagesView(EssentialsMixin, DetailView):
    model = Pages
    template_name = "home/pages_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context

class RegionView(EssentialsMixin, TemplateView):
    template_name = 'home/region.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RegionView, self).get_context_data(*args, **kwargs)
        if self.kwargs.get('region', False):
            try:
                region_code = str.lower(self.kwargs['region'])
                context['requested_region'] = Region.objects.get(country_code=region_code)
                context['obj_error'] = False
            except:
                context['requested_region'] = None
                context['obj_error'] = True
        return context
    
