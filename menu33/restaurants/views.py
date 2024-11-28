from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Restaurant
from menu33.menus.models import FoodItem, DrinkItem, WineItem


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurants-list.html'  # Template for displaying the list of restaurants
    context_object_name = 'restaurants'


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant-details.html'  # Template for restaurant details


class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = ['name', 'description', 'image', 'location']
    template_name = 'restaurants/restaurant-form.html'  # Template for creating a new restaurant
    success_url = reverse_lazy('restaurant-list')

