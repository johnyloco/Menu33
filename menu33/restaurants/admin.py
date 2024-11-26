from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'location')  # Customize fields to display
    search_fields = ('name', 'slug', 'description',)