# Smart Travel - Travel Planning System

A comprehensive travel planning application that helps users discover destinations, plan trips, book accommodations and transportation, and check real-time weather information.

## Complete Setup Guide (Windows 10 Focus)

This step-by-step guide will help you avoid common pitfalls and successfully launch the Smart Travel application.

### Step 1: Install Required Software

1. **Install Python 3.8 or newer**:
   - Download from [python.org](https://www.python.org/downloads/)
   - **IMPORTANT**: Check "Add Python to PATH" during installation ✅

2. **Install PostgreSQL**:
   - Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - **IMPORTANT**: Remember the password you set for the `postgres` user
   - Note your PostgreSQL version (e.g., 14, 15, 16)

3. **Add PostgreSQL to System PATH**:
   - Open File Explorer and navigate to your PostgreSQL bin directory:
     `C:\Program Files\PostgreSQL\<version>\bin`
   - Copy this path
   - Press Win + S, search for "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and paste the PostgreSQL bin path
   - Click OK on all dialogs
   - **IMPORTANT**: Open a new Command Prompt after this step

### Step 2: Set Up the Database

1. **Create the PostgreSQL database**:
   - Open Command Prompt (cmd.exe, not PowerShell)
   - Run: `psql -U postgres -c "CREATE DATABASE travel_planner;"`
   - Enter your postgres password when prompted

2. **Clone the repository**:
   ```
   git clone https://github.com/YourUsername/SMARTTRAVEL.git
   cd SMARTTRAVEL
   ```

### Step 3: Set Up Virtual Environment

1. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```
   venv\Scripts\activate
   ```
   - You should see `(venv)` at the beginning of the command line
   - **IMPORTANT**: Always ensure the virtual environment is activated before running any Python commands

### Step 4: Install Dependencies

1. **Install all required packages**:
   ```
   pip install -r requirements.txt
   ```

### Step 5: Configure the Database Connection

1. **Configure PostgreSQL settings**:
   - Open `travel_planner/travel_planner/settings.py`
   - Locate the `DATABASES` section
   - Update it to use your PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'travel_planner',
           'USER': 'postgres',  # The default superuser
           'PASSWORD': 'your_postgres_password',  # Replace with your actual password
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Step 6: Prepare Django Application

1. **Navigate to the Django project directory**:
   ```
   cd travel_planner
   ```

2. **Apply database migrations**:
   ```
   python manage.py migrate
   ```

3. **Create an admin user**:
   ```
   python manage.py createsuperuser
   ```

### Step 7: Load Sample Data

1. **Load provided sample data**:
   ```
   python manage.py shell -c "exec(open('sample_data.py').read())"
   ```
   - This will populate your database with destinations, accommodations, users, and trips
   - **Note**: Only run this once; it has built-in checks to prevent duplicate data

### Step 8: Run the Development Server

1. **Start the development server**:
   ```
   python manage.py runserver
   ```

2. **Access the website**:
   - Open your browser and go to: http://127.0.0.1:8000/

## Common Issues & Solutions

### Authentication/Login Issues
If you encounter 404 errors when trying to log in or visiting `/accounts/login/`:
- The application URLs are set up to use `/users/login/` instead of Django's default
- URL redirects are in place to handle this, but if issues persist:
- Check `travel_planner/settings.py` has these lines:
  ```python
  LOGIN_URL = 'login'
  LOGIN_REDIRECT_URL = 'home'
  ```

### "No destinations found" or "No destination matches query"
If you see these errors:
- Make sure you've run the sample data script successfully
- Verify data exists by checking:
  ```
  python manage.py shell -c "from destinations.models import Destination; print(Destination.objects.count())"
  ```
- If the count is 0, run the sample data script again

### URL Mapping Issues (404 Errors)
If you see 404 errors for pages like `/trips/` or `/trips/create/`:
- These are redirected to their actual locations: `/bookings/` and `/bookings/create/`
- The redirects are defined in `travel_planner/urls.py`
- If issues persist, verify your URLs match the application's routing structure

### Database Connection Errors
If you see "password authentication failed" or "database does not exist":
1. Verify PostgreSQL is running (Windows Services)
2. Check your database credentials in `settings.py`
3. Ensure the `travel_planner` database exists:
   ```
   psql -U postgres -c "\l"
   ```
4. If not, create it:
   ```
   psql -U postgres -c "CREATE DATABASE travel_planner;"
   ```

### Command Prompt vs PowerShell
- Some commands (especially with `<` input redirection) work differently in PowerShell
- For simplicity, use Command Prompt (cmd.exe) instead of PowerShell
- All instructions in this guide are written for Command Prompt

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
- PostgreSQL (Database)
- Bootstrap 5 (Front-end framework)
- Visual Crossing Weather API (Weather data)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Weather data provided by [Visual Crossing Weather API](https://www.visualcrossing.com/)
- Images from [Unsplash](https://unsplash.com/)
