"""DSCryptoMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from coins.views import dashboard, add_exchange, add_coin, issues, rules, add_rule_form, add_rule_submit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('add_exchange', add_exchange, name='add_exchange'),
    path('add_coin', add_coin, name='add_coin'),
    path('issues', issues, name='issues'),
    path('rules', rules, name='rules'),
    path('add_rule/<str:coin>_<str:exchange>', add_rule_form, name='add_rule_form'),
    path('add_rule', add_rule_submit, name='add_rule_submit')
]
