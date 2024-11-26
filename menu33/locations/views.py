from django.shortcuts import render


def restaurant_location(request):
    return render(request, 'locations/location.html')
