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
            # daily_permission = Permission.objects.get(codename="can_view_daily_report")
            # user.user_permissions.add(daily_permission)
            
            # Regional Permission Logic
            host = request.get_host()
            
            # Define Permission Lists (Only Free Reports)
            AUS_PERMISSIONS = [
                "can_au_mining_report",
                "can_au_dividend_income_report",
                "can_au_growth_report",
                "can_us_equity_(au)",
                "can_under_25_cents_report"
            ]

            CAN_PERMISSIONS = [
                "can_us_equity_(ca)",
                "can_penny_report",
                "can_us_equity",
                "can_mining_report",
                "can_daily_report",
                "can_growth_report",
                "can_dividend_report"
            ]
            
            permissions_to_add = []
            if host.endswith('.com.au'):
                print(f"Assigning AUSTRALIA permissions for host: {host}")
                permissions_list = AUS_PERMISSIONS
            else:
                print(f"Assigning CANADA/GLOBAL permissions for host: {host}")
                permissions_list = CAN_PERMISSIONS

            for codename in permissions_list:
                try:
                    perm = Permission.objects.get(codename=codename)
                    permissions_to_add.append(perm)
                except Permission.DoesNotExist:
                    print(f"Warning: Permission '{codename}' not found.")

            if permissions_to_add:
                user.user_permissions.add(*permissions_to_add)

        except Exception as e:
            print(f"Error assigning permissions: {e}")
            pass # Permission not found, skip adding
            
        user.save()
        lead.first_time = True
    
    
    lead.save()

    # Send Welcome Email to User
    try:
        login_url = request.build_absolute_uri(reverse('account_login'))
        subject = 'Welcome to V2U Research - Your Free Trial Started'
        message = f"""Hi {_data['firstName']},

Thank you for starting your 7-Day Free Trial with V2U Research.

Your account has been created successfully.
Username: {_data['email']}
Password: {user_password}

You can login here: {login_url}

Best regards,
V2U Research Team
"""
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [_data['email']], fail_silently=True)
    except Exception as e:
        print(f"Error sending user email: {e}")

    # Send Notification to Admin
    try:
        admin_subject = f"New Free Trial Lead: {_data['firstName']} {_data['lastName']}"
        admin_message = f"""New Lead Details:
Name: {_data['firstName']} {_data['lastName']}
Email: {_data['email']}
Phone: {_data['phone']}
Source: {lead.source}
"""
        # send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=True)
        send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, ['info@v2uresearch.com.au'], fail_silently=True)

    except Exception as e:
        print(f"Error sending admin email: {e}")

    return redirect('thankyou')

def thank_you(request):
    return render(request, 'marketing/thankyou.html')