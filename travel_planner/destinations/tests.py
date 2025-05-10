from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from .models import Destination
from .utils import get_current_weather, get_weather_forecast
from unittest.mock import patch
import json

class WeatherAPITests(TestCase):
    def setUp(self):
        # Create test destination
        self.destination = Destination.objects.create(
            name="Test City",
            city="London",
            country="UK",
            description="A test destination",
            avg_temperature=15.0,
            best_time_to_visit="Summer",
            popularity_score=4.5
        )
        
    @patch('urllib.request.urlopen')
    def test_get_current_weather(self, mock_urlopen):
        # Mock response data
        mock_weather_data = {
            "currentConditions": {
                "temp": 20.5,
                "conditions": "Partly cloudy",
                "icon": "partly-cloudy-day",
                "humidity": 65,
                "windspeed": 10
            }
        }
        
        # Set up the mock
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = json.dumps(mock_weather_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        
        # Call the function
        weather = get_current_weather("London", "UK")
        
        # Check results
        self.assertEqual(weather["temperature"], 20.5)
        self.assertEqual(weather["description"], "Partly cloudy")
        self.assertEqual(weather["icon"], "02d")  # Mapped from partly-cloudy-day
        self.assertEqual(weather["humidity"], 65)
        self.assertEqual(weather["wind_speed"], 10)
        
    @patch('urllib.request.urlopen')
    def test_get_weather_forecast(self, mock_urlopen):
        # Mock response data
        mock_forecast_data = {
            "days": [
                {
                    "datetime": "2023-07-10",
                    "temp": 22,
                    "conditions": "Clear",
                    "icon": "clear-day"
                },
                {
                    "datetime": "2023-07-11",
                    "temp": 24,
                    "conditions": "Rain",
                    "icon": "rain"
                },
                {
                    "datetime": "2023-07-12",
                    "temp": 20,
                    "conditions": "Cloudy",
                    "icon": "cloudy"
                }
            ]
        }
        
        # Set up the mock
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = json.dumps(mock_forecast_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        
        # Call the function
        forecast = get_weather_forecast("London", "UK", 3)
        
        # Check results
        self.assertEqual(len(forecast), 3)
        self.assertEqual(forecast[0]["date"], "2023-07-10")
        self.assertEqual(forecast[0]["temperature"], 22)
        self.assertEqual(forecast[0]["description"], "Clear")
        self.assertEqual(forecast[0]["icon"], "01d")  # Mapped from clear-day
        
        self.assertEqual(forecast[1]["date"], "2023-07-11")
        self.assertEqual(forecast[1]["description"], "Rain")
        self.assertEqual(forecast[1]["icon"], "09d")  # Mapped from rain

class WeatherViewTests(TestCase):
    def setUp(self):
        # Create test destination
        self.destination = Destination.objects.create(
            name="Test City",
            city="London",
            country="UK",
            description="A test destination",
            avg_temperature=15.0,
            best_time_to_visit="Summer",
            popularity_score=4.5
        )
    
    @patch('destinations.utils.get_current_weather')
    @patch('destinations.utils.get_weather_forecast')
    def test_destination_weather_view(self, mock_forecast, mock_current):
        # Mock the weather data
        mock_current.return_value = {
            "temperature": 17.1,  # Match the actual value from the API
            "description": "Sunny",
            "icon": "01d",
            "humidity": 60,
            "wind_speed": 5,
            "icon_url": "http://openweathermap.org/img/w/01d.png"
        }
        
        mock_forecast.return_value = [
            {
                "date": "2023-07-10",
                "temperature": 22,
                "description": "Sunny",
                "icon": "01d",
                "icon_url": "http://openweathermap.org/img/w/01d.png"
            }
        ]
        
        # Call the view
        url = reverse('destinations:weather', kwargs={'destination_id': self.destination.id})
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destinations/weather.html')
        
        # Check context data
        self.assertEqual(response.context['destination'], self.destination)
        self.assertEqual(response.context['current_weather']['temperature'], 17.1)
        self.assertEqual(len(response.context['forecast']), 5)  # Default forecast length is 5 days
