from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from menu33.menus.models import FoodItem, DrinkItem, WineItem
from menu33.restaurants.models import Restaurant


class RestaurantMenuView(DetailView):
    model = Restaurant
    template_name = 'menus/menu/food-menu.html'
    context_object_name = 'restaurant'

    def get_object(self, **kwargs):
        """
        Fetch the restaurant by ID.
        """
        return get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        """
        Adds categorized menu items to the context.
        """
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()

        # Categorize food items by sections
        context['starters'] = FoodItem.objects.filter(restaurant=restaurant, section='Starters')
        context['main_courses'] = FoodItem.objects.filter(restaurant=restaurant, section='Main Course')
        context['desserts'] = FoodItem.objects.filter(restaurant=restaurant, section='Desserts')
        context['other_items'] = FoodItem.objects.filter(restaurant=restaurant, section='Other')

        # Add categorized menu items
        context['food_items'] = FoodItem.objects.filter(restaurant=restaurant)
        context['drink_items'] = DrinkItem.objects.filter(restaurant=restaurant)
        context['wine_items'] = WineItem.objects.filter(restaurants=restaurant)

        return context


class RestaurantWineMenuView(DetailView):
    model = Restaurant
    template_name = 'menus/menu/wine-menu.html'
    context_object_name = 'restaurant'

    def get_object(self, **kwargs):
        """
        Fetch the restaurant by ID.
        """
        return get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        """
        Adds categorized menu items to the context.
        """
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()

        # Categorize wine items
        context['sparkling_wines'] = WineItem.objects.filter(restaurants=restaurant)
        context['white_wines'] = WineItem.objects.filter(restaurants=restaurant)
        context['rose_wines'] = WineItem.objects.filter(restaurants=restaurant)
        context['red_wines'] = WineItem.objects.filter(restaurants=restaurant)
        context['dessert_wines'] = WineItem.objects.filter(restaurants=restaurant)
        context['fortified_wines'] = WineItem.objects.filter(restaurants=restaurant)

        return context


class RestaurantDrinkView(DetailView):
    model = Restaurant
    template_name = 'menus/menu/drink-menu.html'
    context_object_name = 'restaurant'

    def get_object(self, **kwargs):
        """
        Fetch the restaurant by ID.
        """
        return get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        context['drink_items'] = DrinkItem.objects.filter(restaurant=restaurant)
        return context