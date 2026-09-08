from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'state', 'latitude', 'longitude', 'organization')
    list_filter = ('city', 'state', 'organization')
    search_fields = ('name', 'code', 'city', 'address')
