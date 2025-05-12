from django.contrib import admin
from .models import (
    Trip, Transportation, Itinerary, ItineraryItem, 
    HotelBooking, TransportationBooking, ETicket, PaymentTransaction
)

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    autocomplete_fields = ['attraction']

class TransportationInline(admin.TabularInline):
    model = Transportation
    extra = 0
    show_change_link = True

class HotelBookingInline(admin.TabularInline):
    model = HotelBooking
    extra = 0
    show_change_link = True
    fields = ('accommodation', 'check_in_date', 'check_out_date', 'total_cost', 'status', 'is_paid')
    readonly_fields = ('booking_reference',)

class TransportationBookingInline(admin.TabularInline):
    model = TransportationBooking
    extra = 0
    show_change_link = True
    fields = ('transportation', 'booking_reference', 'status', 'is_paid')

class ETicketInline(admin.TabularInline):
    model = ETicket
    extra = 0
    show_change_link = True
    fields = ('ticket_type', 'ticket_number', 'issue_date')
    readonly_fields = ('ticket_number', 'issue_date')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'start_date', 'end_date', 'budget', 'is_completed')
    list_filter = ('is_completed', 'destination__country', 'start_date')
    search_fields = ('title', 'user__username', 'user__email', 'destination__name')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'destination', 'start_date', 'end_date', 'is_completed')
        }),
        ('Additional Details', {
            'fields': ('accommodation', 'budget', 'notes', 'created_at')
        }),
    )
    inlines = [TransportationInline, HotelBookingInline, TransportationBookingInline, ETicketInline]
    autocomplete_fields = ['user', 'destination', 'accommodation']

@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('trip', 'type', 'provider', 'departure_location', 'arrival_location', 'departure_time', 'cost')
    list_filter = ('type', 'departure_time', 'trip__destination')
    search_fields = ('trip__title', 'provider', 'departure_location', 'arrival_location', 'booking_reference')
    date_hierarchy = 'departure_time'
    autocomplete_fields = ['trip']

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('trip', 'day', 'date', 'get_destination')
    list_filter = ('trip__destination',)
    search_fields = ('trip__title', 'trip__user__username')
    inlines = [ItineraryItemInline]
    autocomplete_fields = ['trip']
    
    def get_destination(self, obj):
        return obj.trip.destination
    get_destination.short_description = 'Destination'
    get_destination.admin_order_field = 'trip__destination__name'

@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ('get_trip', 'get_day', 'attraction', 'custom_activity', 'start_time', 'end_time')
    list_filter = ('itinerary__trip__destination',)
    search_fields = ('attraction__name', 'custom_activity', 'itinerary__trip__title')
    autocomplete_fields = ['itinerary', 'attraction']
    
    def get_trip(self, obj):
        return obj.itinerary.trip.title
    get_trip.short_description = 'Trip'
    
    def get_day(self, obj):
        return f"Day {obj.itinerary.day}"
    get_day.short_description = 'Day'

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    show_change_link = True
    fields = ('payment_method', 'amount', 'status', 'transaction_id', 'created_at')
    readonly_fields = ('transaction_id', 'created_at')

@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'trip', 'accommodation', 'check_in_date', 'check_out_date', 'total_cost', 'status', 'is_paid')
    list_filter = ('status', 'is_paid', 'check_in_date', 'accommodation__destination')
    search_fields = ('trip__user__username', 'trip__title', 'accommodation__name', 'booking_reference')
    readonly_fields = ('booking_reference', 'booking_date')
    date_hierarchy = 'check_in_date'
    inlines = [PaymentTransactionInline]
    autocomplete_fields = ['trip', 'accommodation']
    
    def get_user(self, obj):
        return obj.trip.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'trip__user__username'

@admin.register(TransportationBooking)
class TransportationBookingAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'trip', 'get_transportation_type', 'status', 'is_paid', 'booking_reference')
    list_filter = ('status', 'is_paid', 'transportation__type')
    search_fields = ('trip__user__username', 'trip__title', 'booking_reference', 'transportation__provider')
    readonly_fields = ('booking_reference', 'booking_date')
    inlines = [PaymentTransactionInline]
    autocomplete_fields = ['trip', 'transportation']
    
    def get_user(self, obj):
        return obj.trip.user
    get_user.short_description = 'User'
    
    def get_transportation_type(self, obj):
        return obj.transportation.type
    get_transportation_type.short_description = 'Type'

@admin.register(ETicket)
class ETicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'ticket_type', 'ticket_number', 'issue_date')
    list_filter = ('ticket_type', 'issue_date')
    search_fields = ('user__username', 'user__email', 'trip__title', 'ticket_number')
    readonly_fields = ('ticket_number', 'issue_date')
    date_hierarchy = 'issue_date'
    autocomplete_fields = ['user', 'trip', 'hotel_booking', 'transportation_booking']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_type', 'payment_method', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'payment_method', 'booking_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'transaction_id', 'card_last_digits')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    autocomplete_fields = ['user', 'hotel_booking', 'transportation_booking']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'booking_type', 'amount', 'payment_method', 'status')
        }),
        ('Booking Details', {
            'fields': ('hotel_booking', 'transportation_booking')
        }),
        ('Payment Information', {
            'fields': ('transaction_id', 'card_last_digits', 'created_at', 'updated_at')
        }),
    )
