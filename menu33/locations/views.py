from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from menu33.locations.models import Location


def restaurant_location(request):
    return render(request, 'locations/location.html')


def location_view(request, restaurant_pk):
    location = get_object_or_404(
        Location,
        restaurants__id=restaurant_pk,
    )
    context = {
        'restaurant_name': location.restaurants.name,
        'google_maps_embed_url': location.get_embed_url(),  # Pass the embed URL

    }
    return render(request, 'locations/location.html', context)


class AddLocation(LoginRequiredMixin, CreateView):
    model = Location
    template_name = 'locations/location-add.html'
    fields = ['address', 'google_maps', 'city', 'canton']  # Specify fields to be displayed in the form
    success_url = reverse_lazy('location-list')  # Redirect to the location list or any other page after successful creation