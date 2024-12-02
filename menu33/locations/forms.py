from django import forms
from menu33.locations.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['address', 'google_maps', 'city', 'canton']