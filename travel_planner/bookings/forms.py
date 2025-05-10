from django import forms
from .models import Trip, Transportation, Itinerary, ItineraryItem, HotelBooking, TransportationBooking, ETicket
from destinations.models import Destination, Accommodation

class TripForm(forms.ModelForm):
    """
    Form for creating a new trip
    """
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'end_date', 'destination', 'accommodation', 'budget', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class TransportationForm(forms.ModelForm):
    """
    Form for adding transportation to a trip
    """
    class Meta:
        model = Transportation
        fields = ['type', 'provider', 'departure_location', 'arrival_location', 
                 'departure_time', 'arrival_time', 'cost']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class HotelBookingForm(forms.ModelForm):
    """
    Form for booking a hotel
    """
    class Meta:
        model = HotelBooking
        fields = ['accommodation', 'check_in_date', 'check_out_date', 'guests', 
                 'room_type', 'total_cost', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests for the hotel?'}),
        }
        
    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)
        if trip:
            # If there's a trip, limit accommodation choices to the trip's destination
            self.fields['accommodation'].queryset = Accommodation.objects.filter(destination=trip.destination)
            # Set initial dates based on trip dates
            self.fields['check_in_date'].initial = trip.start_date
            self.fields['check_out_date'].initial = trip.end_date
            # If trip already has an accommodation, set it as default
            if trip.accommodation:
                self.fields['accommodation'].initial = trip.accommodation

class TransportationBookingForm(forms.ModelForm):
    """
    Form for booking transportation
    """
    class Meta:
        model = TransportationBooking
        fields = ['transportation', 'passenger_names']
        widgets = {
            'passenger_names': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Enter passenger names, one per line'
            }),
        }
        
    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)
        if trip:
            # If there's a trip, limit transportation choices to the trip's transportations
            self.fields['transportation'].queryset = Transportation.objects.filter(trip=trip)

class PaymentForm(forms.Form):
    """
    Form for processing payments
    """
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(
        max_length=16, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Card Number'})
    )
    expiry_date = forms.CharField(
        max_length=5, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'CVV'})
    )
    cardholder_name = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Cardholder Name'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'credit_card':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')
            cardholder_name = cleaned_data.get('cardholder_name')
            
            if not card_number or not expiry_date or not cvv or not cardholder_name:
                raise forms.ValidationError("All credit card fields are required.")
                
        return cleaned_data 