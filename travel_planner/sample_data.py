"""
Script to populate the database with sample data for the travel planner application.
Run this script with:
    python manage.py shell < sample_data.py
"""

import os
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_planner.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth.models import User
from destinations.models import Destination, Accommodation, Attraction
from reviews.models import DestinationReview, AccommodationReview, AttractionReview
from users.models import UserProfile, TravelPreference
from bookings.models import Trip, Transportation, Itinerary, ItineraryItem

# Check if we already have data to avoid duplicates
if Destination.objects.count() > 0:
    print("Data already exists. Exiting to avoid duplicates.")
    exit()

print("Creating sample data...")

# Create destinations
destinations = [
    {
        'name': 'Eiffel Tower', 
        'city': 'Paris', 
        'country': 'France', 
        'description': 'The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.',
        'avg_temperature': 15.5,
        'best_time_to_visit': 'Spring (April-June)',
        'popularity_score': 4.8
    },
    {
        'name': 'Santorini', 
        'city': 'Thera', 
        'country': 'Greece', 
        'description': 'Santorini is one of the Cyclades islands in the Aegean Sea. It was devastated by a volcanic eruption in the 16th century BC, forever shaping its rugged landscape.',
        'avg_temperature': 23.0,
        'best_time_to_visit': 'Late Spring and Early Fall',
        'popularity_score': 4.9
    },
    {
        'name': 'Grand Canyon', 
        'city': 'Arizona', 
        'country': 'USA', 
        'description': 'The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona, United States. The Grand Canyon is 277 miles long, up to 18 miles wide and attains a depth of over a mile.',
        'avg_temperature': 21.0,
        'best_time_to_visit': 'March to May and September to November',
        'popularity_score': 4.7
    },
    {
        'name': 'Kyoto', 
        'city': 'Kyoto', 
        'country': 'Japan', 
        'description': 'Kyoto, once the capital of Japan, is a city on the island of Honshu. It\'s famous for its numerous classical Buddhist temples, as well as gardens, imperial palaces, Shinto shrines and traditional wooden houses.',
        'avg_temperature': 16.0,
        'best_time_to_visit': 'Cherry blossom season (March-April) or fall foliage season (November)',
        'popularity_score': 4.6
    },
    {
        'name': 'Machu Picchu', 
        'city': 'Cusco Region', 
        'country': 'Peru', 
        'description': 'Machu Picchu is an Incan citadel set high in the Andes Mountains in Peru, above the Urubamba River valley. Built in the 15th century and later abandoned, it\'s renowned for its sophisticated dry-stone walls that fuse huge blocks without the use of mortar.',
        'avg_temperature': 13.0,
        'best_time_to_visit': 'Dry season (May to October)',
        'popularity_score': 4.8
    },
]

created_destinations = []
for dest_data in destinations:
    destination = Destination.objects.create(**dest_data)
    created_destinations.append(destination)
    print(f"Created destination: {destination.name}")

# Create accommodations
accommodation_types = ['hotel', 'hostel', 'apartment', 'resort', 'villa']
for destination in created_destinations:
    for i in range(3):  # 3 accommodations per destination
        accommodation = Accommodation.objects.create(
            destination=destination,
            name=f"{['Luxury', 'Budget', 'Family', 'Cozy', 'Elegant'][i % 5]} {destination.name} {accommodation_types[i % 5].title()}",
            type=accommodation_types[i % 5],
            address=f"{random.randint(1, 999)} {['Main', 'Park', 'Beach', 'Mountain', 'Lake'][i % 5]} St, {destination.city}, {destination.country}",
            price_per_night=random.randint(50, 500),
            rating=round(random.uniform(3.0, 5.0), 1),
            amenities="WiFi, Air Conditioning, Swimming Pool, Restaurant, Fitness Center"
        )
        print(f"Created accommodation: {accommodation.name}")

# Create attractions
attraction_categories = ['nature', 'history', 'culture', 'entertainment', 'food']
for destination in created_destinations:
    for i in range(4):  # 4 attractions per destination
        attraction = Attraction.objects.create(
            destination=destination,
            name=f"{destination.name} {['Park', 'Museum', 'Theater', 'Restaurant', 'Garden'][i % 5]}",
            category=attraction_categories[i % 5],
            description=f"A popular {attraction_categories[i % 5]} attraction in {destination.city}.",
            entrance_fee=random.randint(0, 50),
            opening_hours="9:00 AM - 5:00 PM"
        )
        print(f"Created attraction: {attraction.name}")

# Create users
users = []
for i in range(3):
    username = f"user{i+1}"
    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="password123",
        first_name=["John", "Jane", "Robert", "Lisa", "Michael"][i % 5],
        last_name=["Smith", "Doe", "Johnson", "Brown", "Davis"][i % 5]
    )
    users.append(user)
    
    # Create user profile
    profile = UserProfile.objects.create(
        user=user,
        bio=f"I am {user.first_name} and I love traveling!",
        phone_number=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    )
    
    # Create travel preferences
    TravelPreference.objects.create(
        user=user,
        destination_type=["beach", "mountain", "city", "countryside", "historical"][i % 5],
        budget_preference=["budget", "mid_range", "luxury"][i % 3],
        travel_style=["adventure", "relaxation", "cultural", "food", "eco"][i % 5],
        preferred_activities="Hiking, Swimming, Sightseeing, Local Cuisine",
        dietary_restrictions="None" if i % 2 == 0 else "Vegetarian"
    )
    print(f"Created user: {username}")

# Create trips
start_dates = [
    datetime.now() + timedelta(days=30),
    datetime.now() + timedelta(days=60),
    datetime.now() + timedelta(days=90)
]

for i, user in enumerate(users):
    for j, destination in enumerate(created_destinations[:2]):  # 2 trips per user
        start_date = start_dates[j % 3]
        end_date = start_date + timedelta(days=random.randint(3, 14))
        
        trip = Trip.objects.create(
            user=user,
            title=f"{user.first_name}'s trip to {destination.name}",
            start_date=start_date,
            end_date=end_date,
            destination=destination,
            accommodation=Accommodation.objects.filter(destination=destination).first(),
            budget=random.randint(500, 5000),
            notes=f"Looking forward to visiting {destination.name}!",
            is_completed=False
        )
        
        # Create transportation
        Transportation.objects.create(
            trip=trip,
            type="flight",
            provider="Sample Airlines",
            departure_location=f"{user.first_name}'s Home City",
            arrival_location=destination.city,
            departure_time=start_date - timedelta(hours=5),
            arrival_time=start_date,
            booking_reference=f"BOK{random.randint(10000, 99999)}",
            cost=random.randint(200, 1000)
        )
        
        # Create itinerary
        trip_length = (end_date - start_date).days
        for day in range(1, trip_length + 1):
            itinerary_date = start_date + timedelta(days=day-1)
            itinerary = Itinerary.objects.create(
                trip=trip,
                day=day,
                date=itinerary_date
            )
            
            # Create itinerary items
            attractions = Attraction.objects.filter(destination=destination)
            for hour in range(9, 18, 3):  # Activities throughout the day
                attraction = attractions[random.randint(0, len(attractions) - 1)] if attractions else None
                
                ItineraryItem.objects.create(
                    itinerary=itinerary,
                    attraction=attraction,
                    custom_activity="" if attraction else f"Free time in {destination.city}",
                    start_time=datetime.strptime(f"{hour}:00", "%H:%M").time(),
                    end_time=datetime.strptime(f"{hour+2}:00", "%H:%M").time(),
                    notes="Enjoy the experience!"
                )
        
        print(f"Created trip: {trip.title}")

# Create reviews
for user in users:
    # Destination reviews
    for destination in created_destinations[:3]:  # Review 3 destinations
        DestinationReview.objects.create(
            user=user,
            destination=destination,
            rating=random.randint(3, 5),
            weather_rating=random.randint(3, 5),
            safety_rating=random.randint(3, 5),
            comment=f"I had a wonderful time at {destination.name}. The weather was great and I felt very safe."
        )
    
    # Accommodation reviews
    accommodations = Accommodation.objects.all()[:3]
    for accommodation in accommodations:
        AccommodationReview.objects.create(
            user=user,
            accommodation=accommodation,
            rating=random.randint(3, 5),
            cleanliness_rating=random.randint(3, 5),
            service_rating=random.randint(3, 5),
            value_rating=random.randint(3, 5),
            comment=f"My stay at {accommodation.name} was very comfortable. The staff was friendly and the rooms were clean."
        )
    
    # Attraction reviews
    attractions = Attraction.objects.all()[:3]
    for attraction in attractions:
        AttractionReview.objects.create(
            user=user,
            attraction=attraction,
            rating=random.randint(3, 5),
            value_for_money=random.randint(3, 5),
            comment=f"Visiting {attraction.name} was a highlight of my trip. Highly recommended!"
        )

print("Sample data creation completed!") 