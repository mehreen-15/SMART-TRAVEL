import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_planner.settings')
django.setup()

from destinations.models import Attraction

# IDs of attractions to delete
attraction_ids_to_delete = [
    13,  # Notre-Dame Cathedral (duplicate)
    14,  # Akrotiri Archaeological Site (duplicate)
    15,  # Arashiyama Bamboo Grove (duplicate)
    16,  # Kinkaku-ji (Golden Pavilion) (duplicate)
    4,   # Oia Sunset Point
    5,   # Akrotiri Archaeological Site (in Santorini)
    6,   # Red Beach
    7,   # South Rim Trail
    8,   # Grand Canyon Skywalk
]

print("Deleting problematic attractions...")
for attraction_id in attraction_ids_to_delete:
    try:
        attraction = Attraction.objects.get(id=attraction_id)
        print(f"Deleting: ID {attraction_id} - {attraction.name} (Destination: {attraction.destination.name})")
        attraction.delete()
        print(f"  Successfully deleted attraction ID {attraction_id}")
    except Attraction.DoesNotExist:
        print(f"  Attraction with ID {attraction_id} does not exist")
    except Exception as e:
        print(f"  Error deleting attraction ID {attraction_id}: {e}")

print("\nRemaining attractions:")
for attr in Attraction.objects.all():
    print(f"ID: {attr.id}, Name: {attr.name}, Destination: {attr.destination.name}") 