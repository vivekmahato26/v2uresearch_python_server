from django.shortcuts import render, HttpResponse, redirect
from marketing.models import Lead, Product
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission

def free_trial_page(request):
    return render(request, 'marketing/free-trial-page.html')

def free_trial(request):
    if not request.POST:
        return HttpResponse('Error in loading request')

    _data = {item:value for item,value in request.POST.items()}
    user_password = 'Welcome@v2u'
    
    # Capture User Agent consistently as JSON
    user_agent_str = request.META.get('HTTP_USER_AGENT', 'Unknown')
    user_agent_json = {"browser": user_agent_str}

    lead = Lead(
        first_name = _data['firstName'],
        last_name = _data['lastName'],
        email = _data['email'],
        phone = _data['phone'],
        source = 'Web - Free Trial Popup',
        user_agent = user_agent_json,
        is_free_trial = True,
        setup_password = user_password
    )
    lead.save()

    # Check if user is already an subscriber 
    # or elgible for free-trial,
    # use email to check the eligibility
    try:
        user_obj = User.objects.get(email=_data['email'])
        lead.first_time = False
    except User.DoesNotExist:
        user = User(
            first_name = _data['firstName'],
            last_name = _data['lastName'],
            username = _data['email'],
            email = _data['email'],
        )
        user.set_password(user_password)
        user.is_staff = False
        user.save()
        
        try:
            daily_permission = Permission.objects.get(codename="can_view_daily_report")
            user.user_permissions.add(daily_permission)
        except Permission.DoesNotExist:
            pass # Permission not found, skip adding
            
        user.save()
        lead.first_time = True
    
    lead.save()

    return redirect('thankyou')

def thank_you(request):
    return render(request, 'marketing/thankyou.html')