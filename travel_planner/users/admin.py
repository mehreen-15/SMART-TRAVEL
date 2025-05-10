from django.contrib import admin
from .models import UserProfile, TravelPreference

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(TravelPreference)
class TravelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget_preference', 'travel_style')
    list_filter = ('budget_preference', 'travel_style')
    search_fields = ('user__username', 'destination_type')
