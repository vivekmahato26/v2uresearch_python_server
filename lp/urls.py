from django.urls import path
from .views import free_trial, thank_you, free_trial_page

urlpatterns = [
    path('free-trial-post', free_trial, name='free-trial-popup'),
    path('thank-you', thank_you, name='thankyou'),
    path('free-trial', free_trial_page, name='free-trial-page'),

] 