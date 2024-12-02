from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, RestaurantCreateView, RestaurantEditView, \
    RestaurantDeleteView

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),  # List all restaurants
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),  # Restaurant details
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),  # Create a new restaurant
    path('<int:pk>/edit/', RestaurantEditView.as_view(), name='restaurant-edit'),
    path('<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
]
