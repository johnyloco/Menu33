from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from menu33.menus.models import WineItem
from menu33.restaurants.models import Restaurant


class AddWineItemView(CreateView):
    model = WineItem
    fields = ['name', 'description', 'wine_type', 'region', 'grape_variety', 'vintage', 'price', 'image']
    template_name = 'menus/add_item/wine-add.html'

    def form_valid(self, form):
        wine_item = form.save(commit=False)
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        wine_item.user = self.request.user  # Assign the logged-in user
        wine_item.save()
        wine_item.restaurants.add(restaurant)  # Associate the wine item with the restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('wine-menu', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


class EditWineItemView(UpdateView):
    model = WineItem
    fields = ['name', 'description', 'wine_type', 'region', 'grape_variety', 'vintage', 'price', 'image']
    template_name = 'menus/edit_item/wine-edit.html'

    def get_success_url(self):
        return reverse_lazy('wine-details', kwargs={'pk': self.object.pk})


class DeleteWineItemView(DeleteView):
    model = WineItem
    template_name = 'menus/delete_item/wine-delete.html'

    def get_success_url(self):
        restaurant = self.object.restaurants.first()  # Assuming the item is associated with one restaurant
        return reverse_lazy('wine-menu', kwargs={'restaurant_id': restaurant.id})


class DetailsWineItemView(DetailView):
    model = WineItem
    template_name = 'menus/details_item/wine-details.html'
    context_object_name = 'wine_item'




