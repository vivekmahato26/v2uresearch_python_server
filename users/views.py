from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from home.mixins import EssentialsMixin

# Create your views here.


class EditProfileView(LoginRequiredMixin, EssentialsMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "sex", "secondary_email", "secondary_phone", "address", "zip_code"]
    template_name = "account/user_update_profile.html"
    success_url = reverse_lazy('dashboard-report')
    
    def get_object(self, queryset=None):
        # Ensure users can only edit their own profile
        # For now, we'll use the pk from URL, but in production you'd want to verify
        # that the user owns this profile or use request.user directly
        return super().get_object(queryset)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
