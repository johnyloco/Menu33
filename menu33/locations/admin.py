from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'canton', 'google_maps',)  # Customize fields to display
    search_fields = ('address', 'city', 'canton', 'google_maps',)
