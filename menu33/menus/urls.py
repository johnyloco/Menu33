from django.urls import path
from . import views
from menu33.menus.views.food import AddFoodItem, EditFoodItemView, DeleteFoodItemView, details_food
from .views import AddWineItemView, EditWineItemView, DeleteWineItemView, AddDrinkItemView, \
    EditDrinkItemView, DeleteDrinkItemView
from .views.common import RestaurantMenuView, RestaurantWineMenuView, RestaurantDrinkView

urlpatterns = [

    # Food URLS
    path('restaurants/<int:restaurant_id>/menu/', RestaurantMenuView.as_view(), name='food-menu'),
    path('menus/<int:restaurant_id>/add/', AddFoodItem.as_view(), name='food-add'),
    path('food/<str:username>/menus/<slug:menus_slug>/', views.details_food, name='food-details'),
    path('food/<int:pk>/edit/', EditFoodItemView.as_view(), name='food-edit'),
    path('food/<int:pk>/delete/', DeleteFoodItemView.as_view(), name='food-delete'),

    # Drink URLS

    path('restaurants/<int:restaurant_id>/drinks/', RestaurantDrinkView.as_view(), name='drink-menu'),
    path('menus/<int:restaurant_id>/drink/add/', AddDrinkItemView.as_view(), name='drink-add'),
    path('drink/<str:username>/menus/<slug:menus_slug>/', views.details_drink, name='drink-details'),
    path('drink/<int:pk>/edit/', EditDrinkItemView.as_view(), name='drink-edit'),
    path('drink/<int:pk>/delete/', DeleteDrinkItemView.as_view(), name='drink-delete'),


    path('restaurants/<int:restaurant_id>/wine-menu/', RestaurantWineMenuView.as_view(), name='wine-menu'),
    path('menus/<int:restaurant_id>/wine/add/', AddWineItemView.as_view(), name='wine-add'),
    path('wine/<str:username>/menus/<slug:menus_slug>/', views.details_wine, name='wine-details'),
    path('wine/<int:pk>/edit/', EditWineItemView.as_view(), name='wine-edit'),
    path('wine/<int:pk>/delete/', DeleteWineItemView.as_view(), name='wine-delete'),


]



