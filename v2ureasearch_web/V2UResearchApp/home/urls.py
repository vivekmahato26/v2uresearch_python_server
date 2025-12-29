from django.contrib import admin
from django.urls import path, include
from .views import HomeView, ContactUsView, PagesView, SuccessView
from marketing.views import DashboardProductListView
from reports.views import ReportListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact-us', ContactUsView.as_view(), name='contact_us'),
    path('successful', SuccessView.as_view(), name='success_page'),
    path('pages/<slug:slug>', PagesView.as_view(), name='pages'),
    path('dashboard-report/', ReportListView.as_view(), name='dashboard-report'),
    path('dashboard-product/', DashboardProductListView.as_view(), name='dashboard-product'),
] 