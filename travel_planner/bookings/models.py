from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination, Accommodation, Attraction
import uuid
from django.utils import timezone

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Transportation(models.Model):
    TYPE_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
        ('car', 'Car Rental'),
        ('ferry', 'Ferry'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='transportations')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    provider = models.CharField(max_length=100)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    booking_reference = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.type} from {self.departure_location} to {self.arrival_location}"

class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')
    day = models.PositiveIntegerField()
    date = models.DateField()
    
    def __str__(self):
        return f"Day {self.day} of {self.trip.title}"

class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='items')
    attraction = models.ForeignKey(Attraction, on_delete=models.SET_NULL, null=True, blank=True)
    custom_activity = models.CharField(max_length=200, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        activity = self.attraction.name if self.attraction else self.custom_activity
        return f"{activity} at {self.start_time}"

class HotelBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='hotel_bookings')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveSmallIntegerField(default=1)
    room_type = models.CharField(max_length=100, default="Standard")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_reference = models.CharField(max_length=20, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"HB{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking at {self.accommodation.name} for {self.trip.title}"

class TransportationBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='transport_bookings')
    transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_reference = models.CharField(max_length=20, blank=True)
    passenger_names = models.TextField(help_text="Enter passenger names, one per line")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"TB{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Transport booking for {self.transportation.type} to {self.transportation.arrival_location}"

class ETicket(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('transportation', 'Transportation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='e_tickets')
    ticket_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    hotel_booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    transportation_booking = models.ForeignKey(TransportationBooking, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='tickets/qr_codes/', blank=True, null=True)
    additional_info = models.JSONField(default=dict, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TCKT{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_ticket_type_display()} Ticket: {self.ticket_number}"

class PaymentTransaction(models.Model):
    """
    Model for tracking payment transactions (for demo purposes only)
    """
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=20)  # 'hotel' or 'transportation'
    hotel_booking = models.ForeignKey(HotelBooking, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    transportation_booking = models.ForeignKey(TransportationBooking, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card_last_digits = models.CharField(max_length=4, blank=True, null=True)  # Store only last 4 digits for demo
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Generate unique transaction ID
            self.transaction_id = f"TR{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.get_status_display()}"
