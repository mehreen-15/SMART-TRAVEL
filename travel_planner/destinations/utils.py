"""
Utility functions for destinations app
"""
import urllib.parse
import requests
import urllib.request
import json
from django.conf import settings

def get_destination_image_url(destination):
    """
    Get the image URL for a destination. If the destination has an image,
    return its URL. Otherwise, return a specific, high-quality image from Unsplash.
    """
    if destination.image and hasattr(destination.image, 'url'):
        return destination.image.url
    
    # Fixed image URLs for specific destinations (destination.id based)
    destination_images = {
        1: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Paris
        2: "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Santorini
        3: "https://images.unsplash.com/photo-1474044159687-1ee9f3a51722?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Grand Canyon
        4: "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Kyoto
        5: "https://images.unsplash.com/photo-1478391679764-b2d8b3cd1e94?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Notre-Dame
        6: "https://images.unsplash.com/photo-1607619662634-3ac55ec0e216?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Arashiyama
        7: "https://images.unsplash.com/photo-1624299831638-82c15fcafd2b?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Kinkaku-ji
        8: "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",  # Akrotiri
    }
    
    # Return specific image if we have one for this destination id
    if hasattr(destination, 'id') and destination.id in destination_images:
        return destination_images[destination.id]
    
    # Fallback to Unsplash direct photos rather than dynamic API
    default_destination_images = {
        'beach': "https://images.unsplash.com/photo-1520454974749-611b7248ffdb?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'mountain': "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'city': "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'historic': "https://images.unsplash.com/photo-1552832230-c0197dd311b5?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'default': "https://images.unsplash.com/photo-1500835556837-99ac94a94552?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"
    }
    
    # Check destination description for keywords
    if destination.description:
        if "beach" in destination.description.lower() or "coast" in destination.description.lower():
            return default_destination_images['beach']
        elif "mountain" in destination.description.lower() or "hill" in destination.description.lower():
            return default_destination_images['mountain']
        elif "city" in destination.description.lower() or "urban" in destination.description.lower():
            return default_destination_images['city']
        elif "historic" in destination.description.lower() or "ancient" in destination.description.lower():
            return default_destination_images['historic']
    
    return default_destination_images['default']

def get_attraction_image_url(attraction):
    """
    Get the image URL for an attraction. If the attraction has an image,
    return its URL. Otherwise, return a specific, high-quality image from Unsplash.
    """
    if attraction.image and hasattr(attraction.image, 'url'):
        return attraction.image.url
    
    # Specific attraction images based on name
    attraction_name_images = {
        "Grand Canyon Museum": "https://images.unsplash.com/photo-1602400236313-719c7eac9977?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Desert View Watchtower": "https://images.unsplash.com/photo-1605558774122-3991814ae0dd?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "South Kaibab Trail": "https://images.unsplash.com/photo-1537104780844-0a367d952c4a?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Kinkaku-ji Temple": "https://images.unsplash.com/photo-1598018553943-89dc869bf90d?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Kinkaku-ji (Golden Pavilion)": "https://images.unsplash.com/photo-1624299831638-82c15fcafd2b?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Arashiyama Bamboo Grove": "https://images.unsplash.com/photo-1607619662634-3ac55ec0e216?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Eiffel Tower": "https://images.unsplash.com/photo-1543349689-9a4d426bee8e?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Notre-Dame Cathedral": "https://images.unsplash.com/photo-1478391679764-b2d8b3cd1e94?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Acropolis": "https://images.unsplash.com/photo-1555993539-1732b0258235?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Akrotiri Archaeological Site": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Santorini Museum": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Museum of Prehistoric Thera": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        "Archaeological Museum of Thera": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
    }
    
    # Try case-insensitive name matching for museum attractions
    if "museum" in attraction.name.lower() and "santorini" in attraction.name.lower():
        return attraction_name_images["Santorini Museum"]
    
    # If we have a specific image for this attraction name
    if attraction.name in attraction_name_images:
        return attraction_name_images[attraction.name]
    
    # Fixed image URLs for common categories - using high-quality direct links
    category_images = {
        'nature': "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'history': "https://images.unsplash.com/photo-1569792060731-f8dd883de720?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'culture': "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200", 
        'entertainment': "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'food': "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'museum': "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"
    }
    
    # Check for museum or gallery in the attraction name
    if ("museum" in attraction.name.lower() or "gallery" in attraction.name.lower()):
        return category_images['museum']
    
    # Return category-specific image if available
    if hasattr(attraction, 'category') and attraction.category in category_images:
        return category_images[attraction.category]
    
    # Fallback to a general attraction image
    return "https://images.unsplash.com/photo-1534008897995-27a23e859048?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"

def get_accommodation_image_url(accommodation):
    """
    Get the image URL for an accommodation. If the accommodation has an image,
    return its URL. Otherwise, return a specific, high-quality image from Unsplash.
    """
    if accommodation.image and hasattr(accommodation.image, 'url'):
        return accommodation.image.url
    
    # Fixed image URLs for accommodation types - using high-quality direct links
    accommodation_type_images = {
        'hotel': "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'hostel': "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'apartment': "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'resort': "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
        'villa': "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"
    }
    
    # Return type-specific image if available
    if hasattr(accommodation, 'type') and accommodation.type in accommodation_type_images:
        return accommodation_type_images[accommodation.type]
    
    # Fallback to a general accommodation image
    return "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"

def get_current_weather(city, country):
    """
    Get current weather for a location using Visual Crossing Weather API
    Returns a dictionary with weather data
    """
    try:
        # Format the location query
        location = f"{city},{country}"
        query = urllib.parse.quote(location)
        
        # Use Visual Crossing Weather API
        api_key = settings.VISUALCROSSING_WEATHER_API_KEY
        if not api_key or api_key == 'your_api_key_here':
            print("Warning: Weather API key is not set properly")
            return {}
            
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{query}?unitGroup=metric&key={api_key}&contentType=json"
        
        # Make API request
        response = urllib.request.urlopen(url)
        
        # Parse the data
        response_content = response.read().decode('utf-8')
        data = json.loads(response_content)
        
        # Extract current weather data
        current_data = data.get('currentConditions', {})
        
        if current_data:
            # Map the Visual Crossing data structure to our own
            icon_code = current_data.get('icon', 'cloudy')
            
            # Create weather icon URL (Visual Crossing doesn't provide direct icon URLs)
            icon_mapping = {
                'clear-day': '01d',
                'clear-night': '01n',
                'partly-cloudy-day': '02d',
                'partly-cloudy-night': '02n',
                'cloudy': '03d',
                'rain': '09d',
                'showers': '09d',
                'snow': '13d',
                'fog': '50d',
                'wind': '50d',
                'thunder-rain': '11d',
                'thunder-showers': '11d'
            }
            
            # Use OpenWeatherMap icon format for compatibility with the template
            openweather_icon_code = icon_mapping.get(icon_code, '03d')
            
            weather_info = {
                "temperature": current_data.get('temp', 0),
                "description": current_data.get('conditions', 'Unknown'),
                "icon": openweather_icon_code,
                "humidity": current_data.get('humidity', 0),
                "wind_speed": current_data.get('windspeed', 0),
                "icon_url": f"http://openweathermap.org/img/w/{openweather_icon_code}.png"
            }
            return weather_info
        else:
            # Return empty dictionary if no data found
            print("No current weather data found in API response")
            return {}
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching weather data: {e.code} - {e.reason}")
        return {}
    except urllib.error.URLError as e:
        print(f"URL Error fetching weather data: {e.reason}")
        return {}
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {}

def get_weather_forecast(city, country, days=5):
    """
    Get weather forecast for a location using Visual Crossing Weather API
    Returns a list of daily forecasts
    """
    try:
        # Format the location query
        location = f"{city},{country}"
        query = urllib.parse.quote(location)
        
        # Use Visual Crossing Weather API
        api_key = settings.VISUALCROSSING_WEATHER_API_KEY
        if not api_key or api_key == 'your_api_key_here':
            print("Warning: Weather API key is not set properly")
            return []
            
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{query}?unitGroup=metric&key={api_key}&contentType=json"
        
        # Make API request
        response = urllib.request.urlopen(url)
        
        # Parse the data
        response_content = response.read().decode('utf-8')
        data = json.loads(response_content)
        
        # Process daily forecast data
        daily_data = data.get('days', [])
        daily_forecasts = []
        
        # Icon mapping for consistent icons
        icon_mapping = {
            'clear-day': '01d',
            'clear-night': '01n',
            'partly-cloudy-day': '02d',
            'partly-cloudy-night': '02n',
            'cloudy': '03d',
            'rain': '09d',
            'showers': '09d',
            'snow': '13d',
            'fog': '50d',
            'wind': '50d',
            'thunder-rain': '11d',
            'thunder-showers': '11d'
        }
        
        # Create a forecast list for each day
        for i, day in enumerate(daily_data):
            if i >= days:  # Limit to requested number of days
                break
                
            # Format date
            date = day.get('datetime', '')
            
            # Map icon code
            icon_code = day.get('icon', 'cloudy')
            openweather_icon_code = icon_mapping.get(icon_code, '03d')
            
            # Create forecast entry
            forecast = {
                "date": date,
                "temperature": day.get('temp', 0),
                "description": day.get('conditions', 'Unknown'),
                "icon": openweather_icon_code,
                "icon_url": f"http://openweathermap.org/img/w/{openweather_icon_code}.png"
            }
            
            daily_forecasts.append(forecast)
            
        return daily_forecasts
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching weather forecast: {e.code} - {e.reason}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error fetching weather forecast: {e.reason}")
        return []
    except Exception as e:
        print(f"Error fetching weather forecast: {e}")
        return [] 