from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from .models import Destination, Accommodation, Attraction
from .utils import get_destination_image_url, get_attraction_image_url, get_accommodation_image_url, get_current_weather, get_weather_forecast
from django.urls import reverse

# Create your views here.

def destination_list(request):
    try:
        destinations = Destination.objects.all()
        
        # Apply filters if provided
        region = request.GET.get('region', '')
        budget = request.GET.get('budget', '')
        activity = request.GET.get('activity', '')
        
        if region:
            # Map regions to countries or cities for filtering
            region_mapping = {
                'europe': ['France', 'Italy', 'Greece', 'Spain', 'Germany', 'United Kingdom'],
                'asia': ['Japan', 'China', 'Thailand', 'Vietnam', 'India', 'Indonesia'],
                'north_america': ['USA', 'Canada', 'Mexico'],
                'south_america': ['Brazil', 'Peru', 'Argentina', 'Colombia', 'Chile'],
                'africa': ['South Africa', 'Egypt', 'Morocco', 'Kenya', 'Tanzania'],
                'oceania': ['Australia', 'New Zealand', 'Fiji']
            }
            
            if region in region_mapping:
                destinations = destinations.filter(country__in=region_mapping[region])
        
        if budget:
            # Filter accommodations by budget range
            budget_ranges = {
                'budget': (0, 100),  # $0-$100 per night
                'mid_range': (101, 300),  # $101-$300 per night
                'luxury': (301, 10000)  # $301+ per night
            }
            
            if budget in budget_ranges:
                min_price, max_price = budget_ranges[budget]
                # Get destinations with accommodations in the budget range
                destination_ids = Accommodation.objects.filter(
                    price_per_night__gte=min_price,
                    price_per_night__lte=max_price
                ).values_list('destination_id', flat=True).distinct()
                
                destinations = destinations.filter(id__in=destination_ids)
        
        if activity:
            # Filter attractions by activity type
            activity_category_mapping = {
                'beach': 'nature',
                'mountain': 'nature',
                'city': 'entertainment',
                'historical': 'history',
                'food': 'food'
            }
            
            if activity in activity_category_mapping:
                # Get destinations with attractions of the specified category
                destination_ids = Attraction.objects.filter(
                    category=activity_category_mapping[activity]
                ).values_list('destination_id', flat=True).distinct()
                
                destinations = destinations.filter(id__in=destination_ids)
        
        # Determine if filters are active for template rendering
        filters_active = any([region, budget, activity])
        
        # Add image URLs for all destinations
        for destination in destinations:
            destination.image_url = get_destination_image_url(destination)
        
        context = {
            'destinations': destinations,
            'filters_active': filters_active,
            'selected_region': region,
            'selected_budget': budget,
            'selected_activity': activity
        }
        
        return render(request, 'destinations/list.html', context)
    except Exception as e:
        # In case of error, return a basic list without filters
        print(f"Error in destination_list: {e}")
        
        # Get all destinations and add image URLs
        destinations = Destination.objects.all()
        for destination in destinations:
            destination.image_url = get_destination_image_url(destination)
            
        return render(request, 'destinations/list.html', {
            'destinations': destinations,
            'error_message': 'An error occurred while filtering destinations.'
        })

def destination_search(request):
    try:
        query = request.GET.get('q', '')
        destinations = []
        
        if query:
            # Search across multiple fields
            destinations = Destination.objects.filter(
                Q(name__icontains=query) | 
                Q(city__icontains=query) | 
                Q(country__icontains=query) | 
                Q(description__icontains=query)
            ).distinct()
            
            # If no direct matches, try to find attractions or accommodations matching the query
            if not destinations.exists():
                # Search in attractions
                attraction_matches = Attraction.objects.filter(
                    Q(name__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(category__icontains=query)
                ).values_list('destination_id', flat=True).distinct()
                
                # Search in accommodations
                accommodation_matches = Accommodation.objects.filter(
                    Q(name__icontains=query) | 
                    Q(address__icontains=query) |
                    Q(amenities__icontains=query) |
                    Q(type__icontains=query)
                ).values_list('destination_id', flat=True).distinct()
                
                # Combine matches
                all_destination_ids = list(attraction_matches) + list(accommodation_matches)
                
                if all_destination_ids:
                    destinations = Destination.objects.filter(id__in=all_destination_ids)
        
        # Add image URLs
        for destination in destinations:
            destination.image_url = get_destination_image_url(destination)
        
        return render(request, 'destinations/search.html', {
            'destinations': destinations, 
            'query': query,
            'total_results': destinations.count() if query else 0
        })
    except Exception as e:
        # In case of error, return empty search results
        print(f"Error in destination_search: {e}")
        return render(request, 'destinations/search.html', {
            'destinations': [], 
            'query': request.GET.get('q', ''),
            'total_results': 0,
            'error_message': 'An error occurred while searching.'
        })

def destination_detail(request, destination_id):
    try:
        destination = get_object_or_404(Destination, pk=destination_id)
        accommodations = destination.accommodations.all()
        attractions = destination.attractions.all()
        
        # Add image URLs
        destination.image_url = get_destination_image_url(destination)
        
        for accommodation in accommodations:
            accommodation.image_url = get_accommodation_image_url(accommodation)
        
        for attraction in attractions:
            attraction.image_url = get_attraction_image_url(attraction)
        
        # Group attractions by category for better display
        attraction_categories = {}
        for attraction in attractions:
            category = attraction.get_category_display()
            if category not in attraction_categories:
                attraction_categories[category] = []
            attraction_categories[category].append(attraction)
        
        return render(request, 'destinations/detail.html', {
            'destination': destination,
            'accommodations': accommodations,
            'attractions': attractions,
            'attraction_categories': attraction_categories
        })
    except Exception as e:
        # In case of error, redirect to destination list
        print(f"Error in destination_detail: {e}")
        from django.shortcuts import redirect
        return redirect('destinations:list')

def accommodation_detail(request, accommodation_id):
    try:
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        # Get reviews if they exist
        reviews = accommodation.reviews.all() if hasattr(accommodation, 'reviews') else []
        
        # Add image URL
        accommodation.image_url = get_accommodation_image_url(accommodation)
        
        return render(request, 'destinations/accommodation_detail.html', {
            'accommodation': accommodation,
            'reviews': reviews
        })
    except Exception as e:
        # In case of error, redirect to destination list
        print(f"Error in accommodation_detail: {e}")
        from django.shortcuts import redirect
        return redirect('destinations:list')

def attraction_detail(request, attraction_id):
    try:
        attraction = get_object_or_404(Attraction, pk=attraction_id)
        # Get reviews if they exist
        reviews = attraction.reviews.all() if hasattr(attraction, 'reviews') else []
        
        # Add image URL
        attraction.image_url = get_attraction_image_url(attraction)
        
        return render(request, 'destinations/attraction_detail.html', {
            'attraction': attraction,
            'reviews': reviews
        })
    except Exception as e:
        # In case of error, redirect to destination list
        print(f"Error in attraction_detail: {e}")
        from django.shortcuts import redirect
        return redirect('destinations:list')

def get_accommodations_by_destination(request, destination_id):
    """
    API endpoint to get accommodations for a specific destination
    """
    try:
        destination = get_object_or_404(Destination, pk=destination_id)
        accommodations = destination.accommodations.all()
        
        # Prepare the data
        data = []
        for accommodation in accommodations:
            data.append({
                'id': accommodation.id,
                'name': accommodation.name,
                'type': accommodation.type,
                'type_display': accommodation.get_type_display(),
                'price_per_night': accommodation.price_per_night,
                'rating': accommodation.rating,
                'image_url': get_accommodation_image_url(accommodation)
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def search_suggestions(request):
    """
    API endpoint to provide search suggestions for autocomplete
    """
    try:
        query = request.GET.get('q', '')
        suggestions = []
        
        if query and len(query) >= 2:
            # Search in destinations
            destinations = Destination.objects.filter(
                Q(name__icontains=query) | 
                Q(city__icontains=query) | 
                Q(country__icontains=query)
            ).distinct()[:5]  # Limit to 5 results
            
            # Get attractions matching the query
            attractions = Attraction.objects.filter(
                Q(name__icontains=query)
            ).distinct()[:3]  # Limit to 3 results
            
            # Format destination suggestions
            for dest in destinations:
                suggestions.append({
                    'id': dest.id,
                    'text': f"{dest.name}, {dest.city}, {dest.country}",
                    'type': 'destination',
                    'url': reverse('destinations:detail', kwargs={'destination_id': dest.id}),
                    'image': get_destination_image_url(dest)
                })
            
            # Format attraction suggestions
            for attr in attractions:
                suggestions.append({
                    'id': attr.id,
                    'text': f"{attr.name} in {attr.destination.name}",
                    'type': 'attraction',
                    'url': reverse('destinations:attraction_detail', kwargs={'attraction_id': attr.id}),
                    'image': get_attraction_image_url(attr)
                })
        
        return JsonResponse(suggestions, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def attraction_list(request):
    """
    View to display a list of all attractions with category filtering
    """
    try:
        category = request.GET.get('category', 'all')
        
        # Get all attractions
        if category and category != 'all':
            attractions = Attraction.objects.filter(category=category)
        else:
            attractions = Attraction.objects.all()
        
        # Add image URLs
        for attraction in attractions:
            attraction.image_url = get_attraction_image_url(attraction)
        
        return render(request, 'attractions/list.html', {
            'attractions': attractions,
            'selected_category': category
        })
    except Exception as e:
        # In case of error, return a basic list without filters
        print(f"Error in attraction_list: {e}")
        return render(request, 'attractions/list.html', {
            'attractions': [],
            'error_message': 'An error occurred while loading attractions.'
        })

def destination_weather(request, destination_id):
    """
    View to display weather information for a destination
    """
    try:
        destination = get_object_or_404(Destination, pk=destination_id)
        
        # Get current weather data
        current_weather = get_current_weather(destination.city, destination.country)
        
        # Get weather forecast
        forecast = get_weather_forecast(destination.city, destination.country)
        
        # Add image URL for destination
        destination.image_url = get_destination_image_url(destination)
        
        return render(request, 'destinations/weather.html', {
            'destination': destination,
            'current_weather': current_weather,
            'forecast': forecast
        })
    except Exception as e:
        print(f"Error in destination_weather: {e}")
        return redirect('destinations:detail', destination_id=destination_id)

def get_weather_api(request, location):
    """
    API endpoint to get current weather for a location
    Format: /api/weather/city,country/
    """
    try:
        # Parse location string (city,country)
        location_parts = location.split(',')
        if len(location_parts) != 2:
            return JsonResponse({'error': 'Invalid location format. Use city,country'}, status=400)
            
        city = location_parts[0].strip()
        country = location_parts[1].strip()
        
        # Get weather data
        weather_data = get_current_weather(city, country)
        
        if not weather_data:
            return JsonResponse({'error': 'Weather data not found'}, status=404)
            
        return JsonResponse(weather_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
