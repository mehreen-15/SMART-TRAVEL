from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from bookings.admin import (
    TripAdmin, TransportationAdmin, ItineraryAdmin, ItineraryItemAdmin, 
    HotelBookingAdmin, TransportationBookingAdmin, ETicketAdmin, PaymentTransactionAdmin
)
from bookings.models import (
    Trip, Transportation, Itinerary, ItineraryItem, 
    HotelBooking, TransportationBooking, ETicket, PaymentTransaction
)
from destinations.admin import DestinationAdmin, AccommodationAdmin, AttractionAdmin
from destinations.models import Destination, Accommodation, Attraction
from users.admin import TravelPreferenceAdmin
from users.models import TravelPreference, UserProfile
from .admin import TravelPlannerAdminSite, DatabaseStatusAdmin, DatabaseConnectionLogAdmin
from .models import DatabaseStatus, DatabaseConnectionLog

# Create the custom admin site
admin_site = TravelPlannerAdminSite(name='admin')

# Register auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Register bookings models
admin_site.register(Trip, TripAdmin)
admin_site.register(Transportation, TransportationAdmin)
admin_site.register(Itinerary, ItineraryAdmin)
admin_site.register(ItineraryItem, ItineraryItemAdmin)
admin_site.register(HotelBooking, HotelBookingAdmin)
admin_site.register(TransportationBooking, TransportationBookingAdmin)
admin_site.register(ETicket, ETicketAdmin)
admin_site.register(PaymentTransaction, PaymentTransactionAdmin)

# Register destinations models
admin_site.register(Destination, DestinationAdmin)
admin_site.register(Accommodation, AccommodationAdmin)
admin_site.register(Attraction, AttractionAdmin)

# Register users models
admin_site.register(TravelPreference, TravelPreferenceAdmin)

# Register travel_planner models
admin_site.register(DatabaseStatus, DatabaseStatusAdmin)
admin_site.register(DatabaseConnectionLog, DatabaseConnectionLogAdmin) 