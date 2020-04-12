from django.urls import path
from allauth import urls
from . import views as custom_views

import allauth.account.urls

urlpatterns = [
    path('', custom_views.ProfileView.as_view(), name='account_profile'),
]

urlpatterns += urls.urlpatterns