"""
URL configuration for homepage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', views.firstpage, name="firstpage"),
    path('linelogin/', views.linelogin, name="linelogin"),

    path('savepoint/', views.savepoint, name="savepoint"),
    path('savepointapi/', views.savepointapi, name="savepointapi"),
    path('success_savepage/', views.success_savepage, name="success_savepage"),

    path('spendpoint/', views.spendpoint, name="spendpoint"),
    path('spendpointapi/', views.spendpointapi, name="spendpointapi"),
    path('success_spendpage/', views.success_spendpage, name="success_spendpage"),

    # path('', views.home, name='home'),
]
