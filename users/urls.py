from django.contrib import admin
from django.urls import path, include
from .views import EditProfileView

urlpatterns = [
    path('edit/<int:pk>', EditProfileView.as_view(), name='edit-profile'),
] 