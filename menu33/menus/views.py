from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.views.generic import DetailView

from .models import FoodItem, DrinkItem, WineItem
from ..restaurants.models import Restaurant


def add_item_view(request):
    """
    Handles adding a FoodItem.
    """
    FormClass = modelform_factory(FoodItem, exclude=('slug',))
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-food')  # Redirect to the same page or a success URL
    else:
        form = FormClass()
    return render(request, 'menus/add-food.html', {'form': form})


def details_food(request, username, menus_slug):
    """
    Displays details for a specific FoodItem.
    """
    food_item = get_object_or_404(FoodItem, slug=menus_slug)
    return render(request, 'menus/food-details.html', {'food_item': food_item})


def manage_food(request, username, menus_slug):
    """
    Handles editing a specific FoodItem.
    """
    food_item = get_object_or_404(FoodItem, slug=menus_slug)
    FormClass = modelform_factory(FoodItem, exclude=('slug',))

    if request.method == "POST":
        form = FormClass(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('details-food', username=username, menus_slug=menus_slug)
    else:
        form = FormClass(instance=food_item)
    return render(request, 'menus/edit-food.html', {'form': form, 'food_item': food_item})


def delete_food(request, username, menus_slug):
    """
    Handles deleting a specific FoodItem.
    """
    food_item = get_object_or_404(FoodItem, slug=menus_slug)

    if request.method == "POST":
        food_item.delete()
        return redirect('add-food')  # Redirect to add-food or another page

    return render(request, 'menus/delete-food.html', {'food_item': food_item})


class RestaurantMenuView(DetailView):
    model = Restaurant
    template_name = 'menus/restaurant-menu.html'
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

