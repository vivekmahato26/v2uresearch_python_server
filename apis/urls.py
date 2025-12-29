from django.contrib import admin
from django.urls import path, include
from .views import SetCookieApiView

urlpatterns = [
    path('set-cookie', SetCookieApiView.as_view(), name='set_cookie'),
] 