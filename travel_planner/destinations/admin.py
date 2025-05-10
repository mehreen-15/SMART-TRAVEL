from django.contrib import admin
from .models import Destination, Accommodation, Attraction

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'popularity_score')
    list_filter = ('country',)
    search_fields = ('name', 'city', 'country', 'description')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'type', 'price_per_night', 'rating')
    list_filter = ('type', 'destination__country')
    search_fields = ('name', 'destination__name', 'destination__city')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'category', 'entrance_fee')
    list_filter = ('category', 'destination__country')
    search_fields = ('name', 'description', 'destination__name')
