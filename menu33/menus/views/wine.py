from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from menu33.menus.forms import WineItemForm
from menu33.menus.models import WineItem
from menu33.restaurants.models import Restaurant


class AddWineItemView(CreateView):
    model = WineItem
    form_class = WineItemForm
    template_name = 'menus/add_item/wine-add.html'

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
        return reverse_lazy('wine-menu', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


class EditWineItemView(UpdateView):
    model = WineItem
    form_class = WineItemForm
    template_name = 'menus/edit_item/wine-edit.html'

    def get_queryset(self):
        return WineItem.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('drink-menu', kwargs={'restaurant_id': self.object.restaurant.id})


class DeleteWineItemView(DeleteView):
    model = WineItem
    form_class = WineItemForm
    template_name = 'menus/delete_item/wine-delete.html'

    def get_success_url(self):
        restaurant = self.object.restaurants.first()  # Assuming the item is associated with one restaurant
        return reverse_lazy('wine-menu', kwargs={'restaurant_id': restaurant.id})


def details_wine(request, username, menus_slug):
    print("Username:", username)
    print("Slug:", menus_slug)
    wine_item = get_object_or_404(WineItem, slug=menus_slug)

    return render(request, 'menus/details_item/wine-details.html', {'wine_item': wine_item})



