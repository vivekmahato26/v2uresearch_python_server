from django.contrib import admin
from django.urls import path, include
from reports.views import ReportDetailView

urlpatterns = [
    path('<slug:slug>', ReportDetailView.as_view(), name='report-detail'),
] 