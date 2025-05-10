from django.contrib import admin
from .models import DestinationReview, AccommodationReview, AttractionReview

@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'weather_rating', 'safety_rating', 'created_at')
    list_filter = ('rating', 'weather_rating', 'safety_rating', 'destination__country')
    search_fields = ('destination__name', 'user__username', 'comment')
    date_hierarchy = 'created_at'

@admin.register(AccommodationReview)
class AccommodationReviewAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'rating', 'cleanliness_rating', 'service_rating', 'created_at')
    list_filter = ('rating', 'cleanliness_rating', 'service_rating')
    search_fields = ('accommodation__name', 'user__username', 'comment')
    date_hierarchy = 'created_at'

@admin.register(AttractionReview)
class AttractionReviewAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'user', 'rating', 'value_for_money', 'created_at')
    list_filter = ('rating', 'value_for_money')
    search_fields = ('attraction__name', 'user__username', 'comment')
    date_hierarchy = 'created_at'
