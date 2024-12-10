from django import forms
from .models import FoodItem, DrinkItem, WineItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'section', 'gluten_free', 'vegan', 'dairy_free', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'section': forms.Select(attrs={
                'class': 'form-control'
            }),
            'gluten_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vegan': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'dairy_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        labels = {
            'name': 'Food Item Name',
            'description': 'Description',
            'price': 'Price (in CHF)',
            'section': 'Section/Category',
            'gluten_free': 'Gluten-Free',
            'vegan': 'Vegan',
            'dairy_free': 'Dairy-Free',
            'image': 'Upload an Image'
        }


class DrinkItemForm(forms.ModelForm):
    class Meta:
        model = DrinkItem
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter drink item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        labels = {
            'name': 'Drink Name',
            'description': 'Description',
            'price': 'Price (in CHF)',
            'image': 'Upload an Image (optional)'
        }


class WineItemForm(forms.ModelForm):
    class Meta:
        model = WineItem
        fields = [
            'name', 'description', 'wine_type', 'region',
            'grape_variety', 'vintage', 'price', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter wine name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 4
            }),
            'wine_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter wine region (e.g., Bordeaux, Napa Valley)'
            }),
            'grape_variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter grape variety (e.g., Chardonnay, Merlot)'
            }),
            'vintage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vintage year'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL (optional)'
            }),
        }
        labels = {
            'name': 'Wine Name',
            'description': 'Description',
            'wine_type': 'Type of Wine',
            'region': 'Region',
            'grape_variety': 'Grape Variety',
            'vintage': 'Vintage Year',
            'price': 'Price (in CHF)',
            'image': 'Image URL (optional)'
        }



