from django.urls import path

from menu33.common.views import home_page, home

urlpatterns = [
    path('', home_page, name='home_page'),
    path('', home, name="home"),
]