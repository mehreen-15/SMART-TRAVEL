# Smart Travel Planning and Recommendation System

A web-based platform that helps users plan their trips efficiently with personalized recommendations based on user preferences, budget, and real-time travel data.

## Features

- User registration and profile management
- Travel preference settings
- Destination discovery and recommendations
- Accommodation and attraction information
- Real-time weather information and forecasts
- Trip planning and itinerary creation
- Booking management
- User reviews and ratings

## Technologies Used

- Django 5.2 (Python web framework)
- PostgreSQL (Database)
- HTML/CSS (Frontend)
- Bootstrap 5 (UI Framework)
- Pillow (Image processing)
- Django Allauth (Authentication)
- Requests (API integration)
- Visual Crossing Weather API (Weather data)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd travel_planner
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Create a database named 'travel_planner'
   ```
   createdb travel_planner
   ```

5. Update database settings in `travel_planner/settings.py` with your PostgreSQL credentials if needed.

6. Configure API Keys:
   - Sign up for a Visual Crossing Weather API key at https://www.visualcrossing.com/
   - Add your API key to `travel_planner/settings.py`:
     ```python
     VISUALCROSSING_WEATHER_API_KEY = 'your_api_key_here'
     ```

7. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

9. Run the development server:
   ```
   python manage.py runserver
   ```

10. Access the site at http://127.0.0.1:8000/

## Project Structure

- `users/`: User profiles and preferences
- `destinations/`: Destinations, accommodations, attractions, and weather
- `bookings/`: Trip planning and booking management
- `reviews/`: User reviews and ratings

## Weather Features

The Smart Travel system includes comprehensive weather information for all destinations:

- Current weather conditions displayed on destination detail pages
- 5-day weather forecasts for trip planning
- Weather-based activity recommendations
- Detailed weather pages with conditions, humidity, wind speed, and more
- Weather-appropriate packing suggestions

## API Endpoints

- `/destinations/weather/<destination_id>/`: Weather page for a destination
- `/destinations/api/weather/<city>,<country>/`: JSON API for weather data

## Integrated APIs

- [Visual Crossing Weather API](https://www.visualcrossing.com/): Provides current weather and forecast data
- Other planned integrations:
  - Maps integration for location-based services
  - Payment gateway for booking processing 