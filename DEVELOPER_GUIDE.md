# Smart Travel - Developer Documentation

This document explains how the Smart Travel Planning System works from a developer's perspective. It covers the project structure, database design, key files, and how different components work together.

## Project Overview

Smart Travel is a Django-based travel planning application that helps users:
- Discover travel destinations
- Plan trips
- Book accommodations and transportation
- Check weather at destinations
- Generate e-tickets
- Get personalized recommendations
- Process payments (simulated)

## Project Structure

The project follows a standard Django project structure with multiple apps:

```
travel_planner/
├── travel_planner/          # Main project folder
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI config for deployment
├── destinations/            # App for destination-related features
├── trips/                   # App for trip planning features
├── bookings/                # App for accommodation and transportation bookings
├── weather/                 # App for weather information
├── users/                   # App for user profiles and preferences
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
│   ├── base/                # Base templates (layout, home, etc.)
│   ├── destinations/        # Templates for destinations
│   ├── trips/               # Templates for trips
│   ├── bookings/            # Templates for bookings
│   ├── users/               # Templates for users
│   └── weather/             # Templates for weather
└── manage.py                # Django management script
```

## Database Design

The database uses SQLite and includes the following main models:

### Users App
- **User**: Built-in Django user model
- **UserProfile**: Extends the User model with additional fields
- **UserPreference**: Stores user preferences for travel recommendations

### Destinations App
- **Destination**: Stores information about travel destinations (name, description, image, etc.)
- **Attraction**: Stores tourist attractions within destinations
- **Review**: User reviews for destinations

### Trips App
- **Trip**: Stores trip plans (destination, start date, end date, user, etc.)
- **Itinerary**: Detailed daily activities for trips
- **Activity**: Individual activities within an itinerary

### Bookings App
- **HotelBooking**: Stores hotel booking information
- **TransportationBooking**: Stores transportation booking information
- **PaymentTransaction**: Tracks payment status and details for bookings

### Weather App
- **WeatherCache**: Stores cached weather data for destinations

## Key Files Explained

### Settings (travel_planner/settings.py)
- Contains project configuration
- Database settings
- Installed apps
- API keys (Visual Crossing Weather API)
- Static and media file settings

### URLs (travel_planner/urls.py)
- Main URL routing configuration
- Links to app-specific URL configurations

### Models (app_name/models.py)
- Defines database tables as Python classes
- Each app has its own models.py file

### Views (app_name/views.py)
- Contains the logic for handling user requests
- Processes form submissions
- Renders templates with context data

### Templates (templates/app_name/*.html)
- HTML templates that define the user interface
- Use Django template language to display dynamic data
- Extend base templates for consistent layout

### Forms (app_name/forms.py)
- Defines forms for user input
- Handles validation and data processing

### Utils (app_name/utils.py)
- Helper functions used by views and models
- Image handling, data processing, etc.

## How It All Works Together

### User Flow

1. **User Registration and Preferences**:
   - Users register through the `users` app
   - Set travel preferences (budget, style, interests)
   
2. **Destination Discovery**:
   - `destinations` app handles browsing and searching
   - Destinations are filtered based on user preferences
   
3. **Trip Planning**:
   - `trips` app manages trip creation and itineraries
   - Users select destinations and dates
   
4. **Booking Process**:
   - `bookings` app handles hotel and transportation bookings
   - Users select options and input details
   
5. **Payment Processing**:
   - Payment simulation happens in `bookings` app
   - `PaymentTransaction` model tracks payment status
   
6. **E-Ticket Generation**:
   - E-tickets are generated for confirmed bookings
   - Users can download or print tickets

### Authentication System

- Uses Django's built-in authentication system
- `UserProfile` model extends the User model
- Login, logout, and registration handled by `users` app

### Recommendation System

- Based on `UserPreference` model
- Uses a simple rule-based algorithm in `recommendations.py`
- Recommendations displayed on home page and profile

### Weather Integration

- Uses Visual Crossing Weather API
- Weather data is cached to reduce API calls
- `weather` app handles API requests and data display

## Database Relationships

### One-to-One Relationships
- User ↔ UserProfile

### One-to-Many Relationships
- User → UserPreference
- User → Trip
- Destination → Attraction
- Trip → Itinerary
- Itinerary → Activity
- User → HotelBooking
- User → TransportationBooking
- HotelBooking → PaymentTransaction
- TransportationBooking → PaymentTransaction

### Many-to-Many Relationships
- Trip ↔ Destination
- User ↔ Destination (via favorites)

## Template Structure

The application uses a base template system:

- `base.html`: Contains common layout elements
- `home.html`: The landing page template
- App-specific templates extend these base templates

Template blocks include:
- `content`: Main page content
- `extra_css`: Page-specific CSS
- `extra_js`: Page-specific JavaScript

## Static Files

Static files are organized by type:
- `css/`: Stylesheets
- `js/`: JavaScript files
- `images/`: Image assets
- `fonts/`: Font files

The project uses Bootstrap 5 for responsive design.

## Form Processing

1. Form classes defined in `forms.py`
2. Views create form instances
3. Templates render forms
4. Views process form submissions
5. Redirect after successful submission

## AJAX and Dynamic Content

Some features use AJAX for dynamic content:
- Weather updates
- Filtering destinations
- Payment processing feedback

## Payment Simulation

Payment processing is simulated:
1. User selects payment method
2. Enters payment details
3. System creates a `PaymentTransaction` record
4. Transaction is marked as "completed" after a brief delay
5. No actual payment processing occurs

## Adding New Features

To add a new feature:

1. Decide which app it belongs to
2. Update models.py if new data structures are needed
3. Create migrations: `python manage.py makemigrations`
4. Apply migrations: `python manage.py migrate`
5. Add new views in views.py
6. Update URLs in urls.py
7. Create templates in templates/app_name/
8. Add any needed static files

## Common Code Patterns

The project follows these patterns:

### Class-Based Views
Many views use Django's class-based views:
```python
class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
```

### Form Handling
Form handling typically follows this pattern:
```python
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form})
```

### Context Processors
Common context variables are provided via context processors defined in `context_processors.py`.

## Tips for Developers

- Use the Django admin interface to explore and edit data
- Check app-specific `README.md` files for more details
- Look at existing code for examples when adding similar features
- Run tests with `python manage.py test`
- Use Django Debug Toolbar during development

## Common Issues and Solutions

- **Database migration conflicts**: Delete the database and migrations, then recreate them
- **Static files not loading**: Run `python manage.py collectstatic`
- **Form validation errors**: Check form class and template for inconsistencies
- **Template errors**: Check context variables passed to the template

## Conclusion

This documentation provides an overview of the Smart Travel Planning System's architecture and components. By understanding how the different parts work together, you should be able to maintain and extend the application as needed. 