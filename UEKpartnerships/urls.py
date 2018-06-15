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
from university.views import PartnershipAutocomplete

urlpatterns = [
    path('partnership_autocomplete/', login_required(PartnershipAutocomplete.as_view())),
    path('', admin.site.urls),
    path('test500/', login_required(ErrorEmailTest.as_view()))

]
admin.site.site_header = "Współprace Biznesowe UEK"
admin.site.site_title = "Współprace Biznesowe UEK"
