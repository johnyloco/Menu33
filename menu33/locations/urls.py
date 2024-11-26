from django.urls import path

from menu33.locations import views

urlpatterns = [
    path('location/', views.restaurant_location, name='map'),
]