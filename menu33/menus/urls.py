from django.urls import path
from . import views
from .views import RestaurantMenuView, AddFoodItem, EditFoodItemView, DeleteFoodItemView


class EditFoodItem:
    pass


urlpatterns = [
    path('restaurants/<int:restaurant_id>/menu/', RestaurantMenuView.as_view(), name='restaurant-menu'),
    path('<str:username>/menus/add/', AddFoodItem.as_view(), name='add-food'),
    path('<str:username>/menus/<slug:menus_slug>/', views.details_food, name='details-food'),
    path('<str:username>/menus/<slug:menus_slug>/edit/', EditFoodItemView.as_view(), name='edit-food'),
    path('<str:username>/menus/<slug:menus_slug>/delete/', DeleteFoodItemView.as_view(), name='delete-food'),
]
