# Smart Travel - Travel Planning System

A comprehensive travel planning application that helps users discover destinations, plan trips, book accommodations and transportation, and check real-time weather information.

## Features

- **Destination Discovery**: Browse and search for destinations with detailed information
- **Trip Planning**: Create and manage trip itineraries
- **Accommodation & Transportation Booking**: Book hotels and transportation options
- **Weather Information**: View current weather and forecasts for destinations
- **E-Ticket System**: Generate and download e-tickets for bookings
- **User Preferences**: Personalized travel recommendations based on preferences
- **Payment Simulation**: Demo payment processing system

## Technologies Used

- Django (Python web framework)
- Bootstrap 5 (Front-end framework)
- SQLite (Database)
- Visual Crossing Weather API (Weather data)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/KomaiX512/SMARTTRAVEL.git
   cd SMARTTRAVEL
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at `http://localhost:8000`

## API Keys

The application uses the Visual Crossing Weather API for weather data. You can set your API key in the `settings.py` file or use environment variables:

```python
VISUALCROSSING_WEATHER_API_KEY = 'your_api_key_here'
```

## Demo Mode

The application includes a demonstration mode for the payment system. No real payments are processed, and all transactions are simulated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Weather data provided by [Visual Crossing Weather API](https://www.visualcrossing.com/)
- Images from [Unsplash](https://unsplash.com/) 