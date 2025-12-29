from django.contrib import admin
from django.urls import path, include
from .views import SectorDetailView, SectorListView

urlpatterns = [
    path('', SectorListView.as_view(), name='sector-list'),
    path('<slug:slug>', SectorDetailView.as_view(), name='sector-detail'),
] 