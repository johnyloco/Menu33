"""
URL configuration for menu33 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

import menu33


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu33.common.urls')),
    path('menus/', include('menu33.menus.urls')),
    path('accounts/', include('menu33.accounts.urls')),
    path('locations/', include('menu33.locations.urls')),
    path('reservations/', include('menu33.reservations.urls')),
    path('restaurants-list/', include('menu33.restaurants.urls')),
    path('photos/', include('menu33.photos.urls')),

]
