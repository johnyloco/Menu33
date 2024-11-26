from django.urls import path
from . import views
from .views import RestaurantMenuView

urlpatterns = [
    path('restaurants/<int:restaurant_id>/menu/', RestaurantMenuView.as_view(), name='restaurant-menu'),
    path('add/', views.add_item_view, name='add-food'),
    path('<str:username>/menus/<slug:menus_slug>/', views.details_food, name='details-food'),
    path('<str:username>/menus/<slug:menus_slug>/edit/', views.manage_food, name='edit-food'),
    path('<str:username>/menus/<slug:menus_slug>/delete/', views.delete_food, name='delete-food'),
]
