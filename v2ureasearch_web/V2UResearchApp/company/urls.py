from django.contrib import admin
from django.urls import path, include
from .views import SectorDetailView

urlpatterns = [
    path('<slug:slug>', SectorDetailView.as_view(), name='sector-detail'),
] 