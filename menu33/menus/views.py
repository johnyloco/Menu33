from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .models import FoodItem, DrinkItem, WineItem
from ..restaurants.models import Restaurant


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


class AddFoodItem(CreateView):
    model = FoodItem
    fields = ['name', 'description', 'price', 'section']  # Ensure 'section' is included if required
    template_name = 'menus/add-food.html'
    success_url = reverse_lazy('add-food', kwargs={'pk': 1})

    def form_valid(self, form):
        food_item = form.save(commit=False)
        food_item.menu = FoodItem  # Associate the food item with the menu
        food_item.save()
        return super().form_valid(form)


def details_food(request, username, menus_slug):
    """
    Displays details for a specific FoodItem.
    """
    food_item = get_object_or_404(FoodItem, slug=menus_slug)
    return render(request, 'menus/food-details.html', {'food_item': food_item})


class EditFoodItemView(UpdateView):
    model = FoodItem
    fields = ['name', 'description', 'price', 'section']  # Include other fields as necessary
    template_name = 'menus/edit-food.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            FoodItem,
            slug=self.kwargs['menus_slug'],
            menu__owner__username=self.kwargs['username']
        )

    def get_success_url(self):
        return reverse_lazy('details-food', kwargs={
            'username': self.kwargs['username'],
            'menus_slug': self.object.slug
        })


class DeleteFoodItemView(DeleteView):
    model = FoodItem
    template_name = 'menus/delete-food.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            FoodItem,
            slug=self.kwargs['menus_slug'],
            menu__owner__username=self.kwargs['username']
        )

    def get_success_url(self):
        return reverse_lazy('menu-detail', kwargs={
            'username': self.kwargs['username'],
            'menus_slug': self.object.menu.slug
        })




