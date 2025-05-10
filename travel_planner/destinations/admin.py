from django.contrib import admin
from django.utils.html import format_html
from .models import Destination, Accommodation, Attraction

class AccommodationInline(admin.TabularInline):
    model = Accommodation
    extra = 1
    show_change_link = True

class AttractionInline(admin.TabularInline):
    model = Attraction
    extra = 1
    show_change_link = True

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'popularity_score', 'accommodations_count', 'attractions_count', 'display_image')
    list_filter = ('country', 'best_time_to_visit')
    search_fields = ('name', 'city', 'country', 'description')
    readonly_fields = ('display_full_image',)
    inlines = [AccommodationInline, AttractionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'country', 'description', 'best_time_to_visit')
        }),
        ('Statistics', {
            'fields': ('popularity_score', 'avg_temperature')
        }),
        ('Image', {
            'fields': ('image', 'display_full_image')
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Thumbnail'
    
    def display_full_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="max-height: 300px; object-fit: contain; border-radius: 10px;" />', obj.image.url)
        return "No Image"
    display_full_image.short_description = 'Image Preview'
    
    def accommodations_count(self, obj):
        return obj.accommodations.count()
    accommodations_count.short_description = 'Accommodations'
    
    def attractions_count(self, obj):
        return obj.attractions.count()
    attractions_count.short_description = 'Attractions'

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'get_country', 'type', 'price_per_night', 'rating', 'display_image')
    list_filter = ('type', 'destination__country', 'rating')
    search_fields = ('name', 'destination__name', 'destination__city', 'address')
    readonly_fields = ('display_full_image',)
    autocomplete_fields = ['destination']
    fieldsets = (
        ('Basic Information', {
            'fields': ('destination', 'name', 'type', 'address')
        }),
        ('Details', {
            'fields': ('price_per_night', 'rating', 'amenities')
        }),
        ('Image', {
            'fields': ('image', 'display_full_image')
        }),
    )
    
    def get_country(self, obj):
        return obj.destination.country
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'destination__country'
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Thumbnail'
    
    def display_full_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="max-height: 300px; object-fit: contain; border-radius: 10px;" />', obj.image.url)
        return "No Image"
    display_full_image.short_description = 'Image Preview'

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'get_country', 'category', 'entrance_fee', 'display_image')
    list_filter = ('category', 'destination__country')
    search_fields = ('name', 'description', 'destination__name', 'destination__city')
    readonly_fields = ('display_full_image',)
    autocomplete_fields = ['destination']
    fieldsets = (
        ('Basic Information', {
            'fields': ('destination', 'name', 'category')
        }),
        ('Details', {
            'fields': ('description', 'entrance_fee', 'opening_hours')
        }),
        ('Image', {
            'fields': ('image', 'display_full_image')
        }),
    )
    
    def get_country(self, obj):
        return obj.destination.country
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'destination__country'
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Thumbnail'
    
    def display_full_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="max-height: 300px; object-fit: contain; border-radius: 10px;" />', obj.image.url)
        return "No Image"
    display_full_image.short_description = 'Image Preview'
