from django.contrib import admin
from .models import FoodItem, DrinkItem, WineItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'gluten_free', 'dairy_free', 'vegan')
    list_filter = ('gluten_free', 'dairy_free', 'vegan', 'restaurant')
    search_fields = ('name', 'description', 'restaurant__name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    fields = ('restaurant', 'name', 'section', 'description', 'price', 'gluten_free', 'dairy_free', 'vegan', 'image', 'slug')


@admin.register(DrinkItem)
class DrinkItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant',)
    search_fields = ('name', 'description', 'restaurant__name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    fields = ('restaurant', 'name', 'description', 'price', 'image', 'slug')


@admin.register(WineItem)
class WineItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_restaurants', 'price', 'region', 'vintage', 'get_wine_type')
    list_filter = ('region', 'vintage', 'restaurants')
    search_fields = ('name', 'description', 'restaurants__name', 'region', 'grape_variety')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    fields = ('restaurants', 'name', 'description', 'wine_type', 'region', 'grape_variety', 'vintage', 'price', 'image', 'slug')

    def get_restaurants(self, obj):
        return ", ".join([restaurant.name for restaurant in obj.restaurants.all()])
    get_restaurants.short_description = 'Restaurants'

    def get_wine_type(self, obj):
        return obj.get_wine_type_display() if obj.wine_type else "N/A"
    get_wine_type.short_description = 'Wine Type'



