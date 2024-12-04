from django import forms
from .models import FoodItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'section', 'gluten_free', 'vegan', 'dairy_free', 'image']
