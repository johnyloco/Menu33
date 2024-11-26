from django.urls import path
from menu33.restaurants import views
from .views import RestaurantListView, RestaurantDetailView, RestaurantCreateView


urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),  # List all restaurants
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),  # Restaurant details
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),  # Create a new restaurant
]
