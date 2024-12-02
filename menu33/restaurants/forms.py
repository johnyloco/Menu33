from django import forms
from menu33.restaurants.models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'image', 'address', 'google_maps', 'city', 'canton']