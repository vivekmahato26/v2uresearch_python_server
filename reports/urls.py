from django.contrib import admin
from django.urls import path, include
from reports.views import ReportDetailView, FreeReportDetailView, DailyReportListView

urlpatterns = [
    path('research', DailyReportListView.as_view(), name='research'),
    path('research/<slug:slug>', DailyReportListView.as_view(), name='research'),
    path('<slug:slug>', ReportDetailView.as_view(), name='report-detail'),
    path('free/<slug:slug>', FreeReportDetailView.as_view(), name='free-report-detail'),
] 