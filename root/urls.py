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
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from accounts.graph_ql import DRFAuthenticatedGraphQLView


urlpatterns = [
    ############################
    # DJANGO ADMIN URL
    ############################
    path('admin/', admin.site.urls),

    #############################
    # REST API URLS
    #############################

    # account urls
    path('accounts/', include('accounts.urls')),
    # business urls
    path('business/authorization/', include('business.authorization.urls')),
    path('business/inventory/', include('business.inventory.urls')),
    path('business/products/', include('business.products.urls')),
    path('business/delivery/', include('client.delivery.urls')),
    path('business/orders/', include('business.orders.urls')),
    path('business/staff/', include('business.staff_accounts.urls')),
    path('client/checkout/', include('client.checkout.urls')),
    path('client/cart/', include('client.cart.urls')),
    path('', lambda request: JsonResponse({"data": "Welcome to the E-commerce API"})),

    ############################
    # GRAPH-QL URLS
    ############################

    path("graph-ql", DRFAuthenticatedGraphQLView.as_view(graphiql=True))
]
