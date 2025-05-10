from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .models import Trip, Transportation, Itinerary, ItineraryItem, HotelBooking, TransportationBooking, ETicket, PaymentTransaction
from destinations.models import Destination, Accommodation, Attraction
from .forms import TripForm, TransportationForm, HotelBookingForm, TransportationBookingForm, PaymentForm
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import json
import random
import string
from datetime import timedelta, datetime
import time  # For simulating payment processing delay

# Create your views here.

@login_required
def trip_list(request):
    # Get user's trips
    trips = Trip.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'bookings/trip_list.html', {'trips': trips})

@login_required
def create_trip(request):
    """
    View for creating a new trip
    """
    # Get all destinations for the form
    destinations = Destination.objects.all()
    
    # Check if there's a destination ID in the query parameters
    destination_id = request.GET.get('destination')
    accommodation_id = request.GET.get('accommodation')
    
    accommodations = []
    initial_data = {}
    
    # If a destination ID is provided, get accommodations for that destination
    if destination_id:
        try:
            destination = Destination.objects.get(pk=destination_id)
            accommodations = destination.accommodations.all()
            
            # Set initial destination
            initial_data['destination'] = destination.id
            
            # Generate a default title
            initial_data['title'] = f"Trip to {destination.name}"
            
            # If accommodation ID is provided, set it in initial data
            if accommodation_id:
                try:
                    accommodation = Accommodation.objects.get(pk=accommodation_id)
                    if accommodation.destination_id == destination.id:
                        initial_data['accommodation'] = accommodation.id
                except Accommodation.DoesNotExist:
                    pass
                
        except Destination.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            
            # Redirect to trip detail page
            messages.success(request, "Your trip has been created successfully!")
            return redirect('bookings:trip_detail', trip_id=trip.id)
    else:
        form = TripForm(initial=initial_data)
    
    return render(request, 'bookings/create_trip.html', {
        'form': form,
        'destinations': destinations,
        'accommodations': accommodations
    })

@login_required
def trip_detail(request, trip_id):
    # Get trip details
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    transportations = trip.transportations.all()
    itineraries = trip.itineraries.all().order_by('day')
    
    # Get hotel bookings
    hotel_bookings = trip.hotel_bookings.all()
    
    # Get transportation bookings
    transportation_bookings = trip.transport_bookings.all()
    
    # Get e-tickets
    e_tickets = trip.e_tickets.all()
    
    return render(request, 'bookings/trip_detail.html', {
        'trip': trip,
        'transportations': transportations,
        'itineraries': itineraries,
        'hotel_bookings': hotel_bookings,
        'transport_bookings': transportation_bookings,
        'e_tickets': e_tickets
    })

@login_required
def edit_trip(request, trip_id):
    # Placeholder for trip edit view
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    return render(request, 'bookings/edit_trip.html', {'trip': trip})

@login_required
def delete_trip(request, trip_id):
    # Placeholder for trip deletion view
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully.')
        return redirect('bookings:trip_list')
    return render(request, 'bookings/delete_trip.html', {'trip': trip})

@login_required
def itinerary(request, trip_id):
    # Placeholder for itinerary view
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    itineraries = trip.itineraries.all().order_by('day')
    return render(request, 'bookings/itinerary.html', {'trip': trip, 'itineraries': itineraries})

@login_required
def add_itinerary_item(request, trip_id):
    # Placeholder for adding itinerary item view
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    return render(request, 'bookings/add_itinerary_item.html', {'trip': trip})

@login_required
def add_transportation(request, trip_id):
    """
    View for adding transportation to a trip
    """
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            transportation = form.save(commit=False)
            transportation.trip = trip
            transportation.save()
            
            messages.success(request, "Transportation added successfully!")
            return redirect('bookings:trip_detail', trip_id=trip.id)
    else:
        # Set default dates based on trip dates
        initial_data = {
            'departure_time': datetime.combine(trip.start_date, datetime.min.time()),
            'arrival_time': datetime.combine(trip.end_date, datetime.min.time()),
        }
        form = TransportationForm(initial=initial_data)
    
    return render(request, 'bookings/add_transportation.html', {
        'form': form,
        'trip': trip
    })

@login_required
def book_hotel(request, trip_id):
    """
    View for booking a hotel
    """
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = HotelBookingForm(request.POST, trip=trip)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.save()
            
            # Redirect to payment page
            return redirect('bookings:payment', booking_type='hotel', booking_id=booking.id)
    else:
        form = HotelBookingForm(trip=trip)
    
    return render(request, 'bookings/book_hotel.html', {
        'form': form,
        'trip': trip
    })

@login_required
def book_transportation(request, trip_id):
    """
    View for booking transportation
    """
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    # First make sure there are transportations to book
    if not trip.transportations.exists():
        messages.warning(request, "Please add transportation details before booking.")
        return redirect('bookings:add_transportation', trip_id=trip.id)
    
    if request.method == 'POST':
        form = TransportationBookingForm(request.POST, trip=trip)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.save()
            
            # Redirect to payment page
            return redirect('bookings:payment', booking_type='transportation', booking_id=booking.id)
    else:
        form = TransportationBookingForm(trip=trip)
    
    return render(request, 'bookings/book_transportation.html', {
        'form': form,
        'trip': trip
    })

@login_required
def payment(request, booking_type, booking_id):
    """
    View for processing payment (for demonstration purposes only)
    """
    # Get the correct booking based on the type
    if booking_type == 'hotel':
        booking = get_object_or_404(HotelBooking, pk=booking_id)
        trip = booking.trip
        payment_amount = booking.total_cost
        booking_ref = booking.booking_reference
    elif booking_type == 'transportation':
        booking = get_object_or_404(TransportationBooking, pk=booking_id)
        trip = booking.trip
        payment_amount = booking.transportation.cost
        booking_ref = booking.booking_reference
    else:
        messages.error(request, "Invalid booking type.")
        return redirect('bookings:trip_list')
    
    # Ensure the booking belongs to the logged-in user
    if trip.user != request.user:
        messages.error(request, "You don't have permission to access this booking.")
        return redirect('bookings:trip_list')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            
            # Create a payment transaction record
            transaction = PaymentTransaction(
                user=request.user,
                booking_type=booking_type,
                amount=payment_amount,
                payment_method=payment_method,
                status='pending'
            )
            
            # Link to the appropriate booking
            if booking_type == 'hotel':
                transaction.hotel_booking = booking
            elif booking_type == 'transportation':
                transaction.transportation_booking = booking
                
            # For credit card payments, store the last 4 digits (demo only)
            if payment_method == 'credit_card':
                card_number = form.cleaned_data.get('card_number', '')
                if card_number:
                    # Remove spaces and get last 4 digits
                    card_number = card_number.replace(' ', '')
                    transaction.card_last_digits = card_number[-4:] if len(card_number) >= 4 else None
            
            # Save the transaction
            transaction.save()
            
            # Simulate payment processing (would be handled by a payment gateway in a real app)
            time.sleep(1)  # Simulate a brief processing delay
            
            # For demonstration, we'll always mark the payment as successful
            transaction.status = 'completed'
            transaction.save()
            
            # Mark the booking as paid and confirmed
            if booking_type == 'hotel':
                booking.is_paid = True
                booking.status = 'confirmed'
                booking.save()
                
                # Generate e-ticket for hotel booking
                create_eticket(request.user, trip, 'hotel', hotel_booking=booking)
                
            elif booking_type == 'transportation':
                booking.is_paid = True
                booking.status = 'confirmed'
                booking.save()
                
                # Generate e-ticket for transportation booking
                create_eticket(request.user, trip, 'transportation', transportation_booking=booking)
            
            messages.success(
                request, 
                f"Payment processed successfully! Transaction ID: {transaction.transaction_id}. "
                f"Booking reference: {booking_ref}"
            )
            return redirect('bookings:trip_detail', trip_id=trip.id)
    else:
        form = PaymentForm()
    
    # Check for existing payments
    existing_payments = None
    if booking_type == 'hotel':
        existing_payments = PaymentTransaction.objects.filter(hotel_booking=booking).order_by('-created_at')
    elif booking_type == 'transportation':
        existing_payments = PaymentTransaction.objects.filter(transportation_booking=booking).order_by('-created_at')
    
    context = {
        'form': form,
        'booking_type': booking_type.capitalize(),
        'booking': booking,
        'payment_amount': payment_amount,
        'trip': trip,
        'existing_payments': existing_payments
    }
    
    return render(request, 'bookings/payment.html', context)

@login_required
def view_eticket(request, ticket_id):
    """
    View for displaying an e-ticket
    """
    ticket = get_object_or_404(ETicket, pk=ticket_id)
    
    # Ensure the ticket belongs to the logged-in user
    if ticket.user != request.user:
        messages.error(request, "You don't have permission to view this ticket.")
        return redirect('bookings:trip_list')
    
    return render(request, 'bookings/view_eticket.html', {
        'ticket': ticket
    })

@login_required
def download_eticket(request, ticket_id):
    """
    View for downloading an e-ticket as PDF
    """
    ticket = get_object_or_404(ETicket, pk=ticket_id)
    
    # Ensure the ticket belongs to the logged-in user
    if ticket.user != request.user:
        messages.error(request, "You don't have permission to download this ticket.")
        return redirect('bookings:trip_list')
    
    # This is a placeholder for actual PDF generation
    # In a real application, you would use a library like ReportLab or WeasyPrint to generate PDF
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{ticket.ticket_number}.txt"'
    
    lines = [
        f"E-TICKET: {ticket.ticket_number}",
        f"Type: {ticket.get_ticket_type_display()}",
        f"Issue Date: {ticket.issue_date}",
        f"Trip: {ticket.trip.title}",
        f"Passenger: {ticket.user.get_full_name() or ticket.user.username}",
        "",
    ]
    
    if ticket.ticket_type == 'hotel':
        hotel_booking = ticket.hotel_booking
        lines.extend([
            f"HOTEL BOOKING DETAILS",
            f"Hotel: {hotel_booking.accommodation.name}",
            f"Check-in: {hotel_booking.check_in_date}",
            f"Check-out: {hotel_booking.check_out_date}",
            f"Room Type: {hotel_booking.room_type}",
            f"Guests: {hotel_booking.guests}",
            f"Booking Reference: {hotel_booking.booking_reference}",
        ])
    elif ticket.ticket_type == 'transportation':
        transport_booking = ticket.transportation_booking
        transport = transport_booking.transportation
        lines.extend([
            f"TRANSPORTATION DETAILS",
            f"Type: {transport.get_type_display()}",
            f"Provider: {transport.provider}",
            f"From: {transport.departure_location}",
            f"To: {transport.arrival_location}",
            f"Departure: {transport.departure_time}",
            f"Arrival: {transport.arrival_time}",
            f"Booking Reference: {transport_booking.booking_reference}",
            f"Passengers: {transport_booking.passenger_names}",
        ])
    
    response.write("\n".join(lines))
    return response

# Helper functions
def create_eticket(user, trip, ticket_type, hotel_booking=None, transportation_booking=None):
    """
    Helper function to create an e-ticket
    """
    # Create e-ticket
    ticket = ETicket(
        user=user,
        trip=trip,
        ticket_type=ticket_type
    )
    
    if ticket_type == 'hotel':
        ticket.hotel_booking = hotel_booking
    elif ticket_type == 'transportation':
        ticket.transportation_booking = transportation_booking
    
    # Store additional info
    additional_info = {}
    if ticket_type == 'hotel':
        additional_info = {
            'hotel_name': hotel_booking.accommodation.name,
            'check_in': hotel_booking.check_in_date.strftime('%Y-%m-%d'),
            'check_out': hotel_booking.check_out_date.strftime('%Y-%m-%d'),
            'room_type': hotel_booking.room_type,
            'booking_ref': hotel_booking.booking_reference
        }
    elif ticket_type == 'transportation':
        transport = transportation_booking.transportation
        additional_info = {
            'type': transport.get_type_display(),
            'provider': transport.provider,
            'departure': transport.departure_location,
            'arrival': transport.arrival_location,
            'departure_time': transport.departure_time.strftime('%Y-%m-%d %H:%M'),
            'booking_ref': transportation_booking.booking_reference
        }
    
    ticket.additional_info = additional_info
    
    # Generate QR code for the ticket
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add data to QR code
    qr_data = {
        'ticket_number': ticket.ticket_number,
        'type': ticket_type,
        'booking_ref': additional_info.get('booking_ref', '')
    }
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to ticket
    buffer = BytesIO()
    img.save(buffer)
    filename = f'qrcode_{ticket.ticket_number}.png'
    ticket.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
    
    # Save the ticket
    ticket.save()
    
    return ticket
