from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from menu33.menus.forms import DrinkItemForm
from menu33.menus.models import DrinkItem
from menu33.restaurants.models import Restaurant


class AddDrinkItemView(LoginRequiredMixin, CreateView):
    model = DrinkItem
    form_class = DrinkItemForm
    template_name = 'menus/add_item/drink-add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']
        return context

    def form_valid(self, form):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        form.instance.restaurant = restaurant
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('drink-menu', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


def details_drink(request, username, menus_slug):
    print("Username:", username)
    print("Slug:", menus_slug)
    drink_item = get_object_or_404(DrinkItem, slug=menus_slug)

    return render(request, 'menus/details_item/drink-details.html', {'drink_item': drink_item})


class EditDrinkItemView(LoginRequiredMixin, UpdateView):
    model = DrinkItem
    form_class = DrinkItemForm
    template_name = 'menus/edit_item/drink-edit.html'

    def get_queryset(self):
        return DrinkItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('drink-menu', kwargs={'restaurant_id': self.object.restaurant.id})


class DeleteDrinkItemView(LoginRequiredMixin, DeleteView):
    model = DrinkItem
    template_name = 'menus/delete_item/drink-delete.html'

    def get_queryset(self):
        # Restrict deletion to the creator of the drink
        return DrinkItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('drink-menu', kwargs={'restaurant_id': self.object.restaurant.id})


