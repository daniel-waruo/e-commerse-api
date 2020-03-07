""" e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from ..api import FacebookLogin, InstagramLogin, GoogleLogin

urlpatterns = [
    # all auth urls
    path('auth/', include("accounts.urls.auth_urls")),
    # rest auth urls
    path('auth/', include('accounts.urls.rest_auth_urls')),
    # account confirm email override
    path('auth/registration/', include('accounts.urls.registration_urls')),

    path('auth/social/instagram/', InstagramLogin.as_view(), name='ig_login'),
    path('auth/social/google/', GoogleLogin.as_view(), name='g_login'),
    path('auth/social/facebook/', FacebookLogin.as_view(), name='fb_login')
]
