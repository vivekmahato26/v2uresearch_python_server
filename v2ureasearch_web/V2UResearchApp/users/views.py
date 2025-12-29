from django.shortcuts import render
from django.views.generic.edit import UpdateView
from .models import User

# Create your views here.


class EditProfileView(UpdateView):
    model = User
    fields = ["first_name","last_name", "sex", "secondary_email", "secondary_phone", "address", "zip_code"]
    template_name = "account/user_update_profile.html"
