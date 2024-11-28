from django.shortcuts import render, get_object_or_404

from menu33.locations.models import Location


def restaurant_location(request):
    return render(request, 'locations/location.html')


def location_view(request, restaurant_pk):
    location = get_object_or_404(Location, restaurants__id=restaurant_pk)
    context = {
        'restaurant_name': location.restaurants.name,
        'google_maps_embed_url': location.get_embed_url(),  # Pass the embed URL

    }
    return render(request, 'locations/location.html', context)