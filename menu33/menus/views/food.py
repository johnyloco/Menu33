from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from menu33.menus.forms import FoodItemForm
from menu33.menus.models import FoodItem

from menu33.restaurants.models import Restaurant


class AddFoodItem(LoginRequiredMixin, CreateView):
    model = FoodItem
    form_class = FoodItemForm
    template_name = 'menus/add_item/food-add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']  # Pass restaurant_id to context
        return context

    def form_valid(self, form):
        # Get the restaurant instance using the restaurant_id from the URL
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        form.instance.restaurant = restaurant  # Set the restaurant for the food item
        form.instance.user = self.request.user  # Link the food item to the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the food menu for the restaurant
        return reverse_lazy('food-menu', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


def details_food(request, username, menus_slug):
    """
    Displays details for a specific FoodItem.
    """
    food_item = get_object_or_404(FoodItem, slug=menus_slug)
    return render(request, 'menus/details_item/food-details.html', {'food_item': food_item})


class EditFoodItemView(LoginRequiredMixin, UpdateView):
    model = FoodItem
    form_class = FoodItemForm
    template_name = 'menus/edit_item/food-edit.html'

    def get_queryset(self):
        # Restrict editing to the user who created the food item
        return FoodItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        # Redirect to the restaurant's food menu
        return reverse_lazy('food-menu', kwargs={'restaurant_id': self.object.restaurant.id})


class DeleteFoodItemView(LoginRequiredMixin, DeleteView):
    model = FoodItem
    template_name = 'menus/delete_item/food-delete.html'

    def get_queryset(self):
        # Restrict deletion to the user who created the food item
        return FoodItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        # Redirect to the restaurant's food menu
        return reverse_lazy('food-menu', kwargs={'restaurant_id': self.object.restaurant.id})