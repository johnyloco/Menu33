from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RestaurantForm
from .models import Restaurant
from ..locations.forms import LocationForm


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurants-list.html'  # Template for displaying the list of restaurants
    context_object_name = 'restaurants'


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant-details.html'  # Template for restaurant details


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurants/restaurant-create-form.html'
    success_url = reverse_lazy('restaurant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include a location form for inline location creation
        if self.request.POST:
            context['location_form'] = LocationForm(self.request.POST)
        else:
            context['location_form'] = LocationForm()
        return context

    def form_valid(self, form):
        location_form = LocationForm(self.request.POST)
        if location_form.is_valid():
            location = location_form.save()  # Save the location
            form.instance.location = location  # Link the new location to the restaurant
            form.instance.user = self.request.user  # Link the restaurant to the logged-in user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class RestaurantEditView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurants/restaurant-edit-form.html'
    success_url = reverse_lazy('restaurant-list')

    def get_queryset(self):
        # Ensures that only restaurants owned by the logged-in user can be edited
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user  # Reassociate with the logged-in user
        return super().form_valid(form)


class RestaurantDeleteView(LoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurants/restaurant-delete.html'
    success_url = reverse_lazy('restaurant-list')

    def get_queryset(self):
        # Restrict deletion to restaurants owned by the logged-in user
        return super().get_queryset().filter(user=self.request.user)