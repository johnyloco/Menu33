from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from menu33.menus.models import DrinkItem
from menu33.restaurants.models import Restaurant


class AddDrinkItemView(LoginRequiredMixin, CreateView):
    model = DrinkItem
    fields = ['name', 'description', 'price', 'image']
    template_name = 'menus/add_item/drink-add.html'

    def form_valid(self, form):
        drink_item = form.save(commit=False)
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        drink_item.user = self.request.user  # Only logged-in user can create
        drink_item.restaurant = restaurant  # Assign the restaurant
        drink_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restaurant-menu', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


class EditDrinkItemView(LoginRequiredMixin, UpdateView):
    model = DrinkItem
    fields = ['name', 'description', 'price', 'image']
    template_name = 'menus/edit_item/drink-edit.html'

    def get_queryset(self):
        # Restrict editing to the creator of the drink
        return DrinkItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('details-drink', kwargs={'pk': self.object.pk})


class DeleteDrinkItemView(LoginRequiredMixin, DeleteView):
    model = DrinkItem
    template_name = 'menus/delete_item/drink-delete.html'

    def get_queryset(self):
        # Restrict deletion to the creator of the drink
        return DrinkItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('restaurant-menu', kwargs={'restaurant_id': self.object.restaurant.id})


class DetailsDrinkItemView(DetailView):
    model = DrinkItem
    template_name = 'menus/details_item/drink-details.html'
    context_object_name = 'drink_item'
