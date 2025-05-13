import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_planner.settings')
django.setup()

from destinations.models import Destination, Attraction, Accommodation

print("=== Checking for problematic attractions ===")
attractions = Attraction.objects.all()

# Check for attractions with same name as their destination
for attr in attractions:
    if attr.name == attr.destination.name:
        print(f"ID: {attr.id}, Name: {attr.name} - Same name as destination!")
        
# Check for attractions with destination name in attraction name
for attr in attractions:
    if attr.destination.name in attr.name and attr.name != attr.destination.name:
        print(f"ID: {attr.id}, Name: {attr.name} - Contains destination name: {attr.destination.name}")

print("\n=== Listing all attractions ===")
for attr in attractions:
    print(f"ID: {attr.id}, Name: {attr.name}, Destination: {attr.destination.name}") 