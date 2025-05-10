from django.contrib import admin
from .models import Trip, Transportation, Itinerary, ItineraryItem

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed', 'start_date', 'destination__country')
    search_fields = ('title', 'user__username', 'destination__name')
    date_hierarchy = 'start_date'

@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('trip', 'type', 'departure_location', 'arrival_location', 'departure_time')
    list_filter = ('type',)
    search_fields = ('trip__title', 'provider', 'departure_location', 'arrival_location')

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('trip', 'day', 'date')
    list_filter = ('trip__destination',)
    search_fields = ('trip__title',)
    inlines = [ItineraryItemInline]
