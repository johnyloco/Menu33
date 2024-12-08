from django import forms
from .models import FoodItem


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
            'price': 'Price (in $)',
            'section': 'Section/Category',
            'gluten_free': 'Gluten-Free',
            'vegan': 'Vegan',
            'dairy_free': 'Dairy-Free',
            'image': 'Upload an Image'
        }