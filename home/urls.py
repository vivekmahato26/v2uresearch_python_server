from django.contrib import admin
from django.urls import path, include
from .views import HomeView, ContactUsView, PagesView, SuccessView, RegionView, switchCountry, SwitchView, AboutUsView, PaymentView
from marketing.views import DashboardProductListView, ArticlesListView, ArticlesDetailView, LeadExportView
from reports.views import ReportListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('payment/', PaymentView.as_view(), name='payment_page'),
    path('about-us', AboutUsView.as_view(), name='about_us'),
    path('contact-us', ContactUsView.as_view(), name='contact_us'),
    path('successful', SuccessView.as_view(), name='success_page'),
    path('pages/<slug:slug>', PagesView.as_view(), name='pages'),
    path('dashboard-report/', ReportListView.as_view(), name='dashboard-report'),
    path('dashboard-product/', DashboardProductListView.as_view(), name='dashboard-product'),
    path('articles/', ArticlesListView.as_view(), name='articles'), 
    path('article/<slug:slug>', ArticlesDetailView.as_view(), name='article'),
    path('u/download-leads', LeadExportView.as_view(), name='downnload-leads'),
    path('region/<slug:region>', RegionView.as_view(), name='region-view'),
    path('switch/<str:to>', switchCountry, name='switch'),
    ] 