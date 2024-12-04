from django.urls import path
from . import views
from menu33.menus.views.food import AddFoodItem, EditFoodItemView, DeleteFoodItemView, details_food
from .views import AddWineItemView, EditWineItemView, DeleteWineItemView, DetailsWineItemView, AddDrinkItemView, \
    EditDrinkItemView, DeleteDrinkItemView, DetailsDrinkItemView
from .views.common import RestaurantMenuView, RestaurantWineMenuView, RestaurantDrinkView

urlpatterns = [
    # Food URLS
    path('restaurants/<int:restaurant_id>/menu/', RestaurantMenuView.as_view(), name='food-menu'),
    path('menus/<int:restaurant_id>/add/', AddFoodItem.as_view(), name='add-food'),
    path('<str:username>/menus/<slug:menus_slug>/', views.details_food, name='details-food'),
    path('food/<int:pk>/edit/', EditFoodItemView.as_view(), name='edit-food'),
    path('food/<int:pk>/delete/', DeleteFoodItemView.as_view(), name='delete-food'),

    # Wine URLS

    path('restaurants/<int:restaurant_id>/wine-menu/', RestaurantWineMenuView.as_view(), name='wine-menu'),
    path('restaurants/<int:restaurant_id>/wine/add/', AddWineItemView.as_view(), name='wine-add'),
    path('wine/<int:pk>/edit/', EditWineItemView.as_view(), name='wine-edit'),
    path('wine/<int:pk>/delete/', DeleteWineItemView.as_view(), name='wine-delete'),
    path('wine/<int:pk>/', DetailsWineItemView.as_view(), name='wine-details'),

    # Drink URLS

    path('<str:username>/menus/<int:restaurant_id>/add-drink/', RestaurantDrinkView.as_view(), name='drink-menu'),
    path('restaurants/<int:restaurant_id>/drink/add/', AddDrinkItemView.as_view(), name='drink-add'),
    path('<str:username>/menus/<slug:menus_slug>/edit/', EditDrinkItemView.as_view(), name='drink-edit'),
    path('<str:username>/menus/<slug:menus_slug>/delete/', DeleteDrinkItemView.as_view(), name='drink-delete'),
    path('<str:username>/menus/<slug:menus_slug>/', DetailsDrinkItemView.as_view(), name='drink-details'),
]



