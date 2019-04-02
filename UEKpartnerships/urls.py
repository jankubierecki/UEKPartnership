"""UEKpartnerships URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from partnerships.views import ErrorEmailTest
from university.views import PartnershipAutocomplete, CompanyAutocomplete, InstituteUnitAutocomplete

import authorization.views

import django_cas_ng.views

urlpatterns = [
    path('partnership_autocomplete/', login_required(PartnershipAutocomplete.as_view())),
    path('company_autocomplete/', login_required(CompanyAutocomplete.as_view())),
    path('institute_unit_autocomplete/', login_required(InstituteUnitAutocomplete.as_view())),
    path('', admin.site.urls),
    path('test500/', login_required(ErrorEmailTest.as_view())),
    path('accounts/login', django_cas_ng.views.login, name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.logout, name='cas_ng_logout'),
    path('accounts/callback', django_cas_ng.views.callback, name='cas_ng_proxy_callback'),
    path('next_page', authorization.views.next_page, name='next_page'),

]
admin.site.site_header = "Współprace Biznesowe UEK"
admin.site.site_title = "Współprace Biznesowe UEK"
