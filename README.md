# Smart Travel - Travel Planning System

A comprehensive travel planning application that helps users discover destinations, plan trips, book accommodations and transportation, and check real-time weather information.

## How to Run This Project Locally (For Beginners)

This guide provides detailed, step-by-step instructions to get this project running on your local machine, even if you have no previous experience.

### Step 1: Install Required Software

#### For Windows:
1. **Install Python**:
   - Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH" ✅
   - Click "Install Now" and wait for installation to complete

2. **Install Git**:
   - Download Git from [git-scm.com](https://git-scm.com/download/win)
   - Use the default options in the installer

#### For macOS:
1. **Install Python**:
   - Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
   - Run the installer and follow the instructions

2. **Install Git**:
   - If you don't have Homebrew, install it by running this in Terminal:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Then install Git:
     ```
     brew install git
     ```

#### For Linux (Ubuntu/Debian):
1. **Update package list**:
   ```
   sudo apt update
   ```

2. **Install Python and Git**:
   ```
   sudo apt install python3 python3-pip python3-venv git
   ```

### Step 2: Clone the Repository

1. **Open Terminal/Command Prompt**:
   - Windows: Press `Win+R`, type `cmd` and press Enter
   - macOS: Open Terminal from Applications > Utilities
   - Linux: Open Terminal (Ctrl+Alt+T on Ubuntu)

2. **Navigate to where you want to store the project**:
   ```
   cd Documents
   ```

3. **Clone the repository**:
   ```
   git clone https://github.com/KomaiX512/SMARTTRAVEL.git
   ```

4. **Navigate into the project folder**:
   ```
   cd SMARTTRAVEL
   ```

### Step 3: Set Up Virtual Environment

#### For Windows:
1. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```
   venv\Scripts\activate
   ```
   You should see `(venv)` at the beginning of the command line

#### For macOS/Linux:
1. **Create a virtual environment**:
   ```
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   ```
   source venv/bin/activate
   ```
   You should see `(venv)` at the beginning of the command line

### Step 4: Install Dependencies

1. **Install all required packages**:
   ```
   pip install -r requirements.txt
   ```
   This may take a few minutes to complete.

### Step 5: Set Up the Database

1. **Navigate to the Django project directory**:
   ```
   cd travel_planner
   ```

2. **Apply database migrations**:
   ```
   python manage.py migrate
   ```

3. **Create an admin user** (you'll need this to access the admin area):
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create a username, email, and password.

### Step 6: Configure Weather API (Optional)

The app uses Visual Crossing Weather API for weather data. You can:

1. **Sign up for a free API key** at [Visual Crossing](https://www.visualcrossing.com/weather-api)

2. **Open the settings file**:
   - Using a text editor, open `travel_planner/travel_planner/settings.py`
   - Find the line with `VISUALCROSSING_WEATHER_API_KEY` and replace the value with your API key:
     ```python
     VISUALCROSSING_WEATHER_API_KEY = 'your_api_key_here'
     ```

### Step 7: Run the Development Server

1. **Make sure you're in the Django project directory**:
   ```
   cd travel_planner  # Skip if you're already in this directory
   ```

2. **Start the development server**:
   ```
   python manage.py runserver
   ```

3. **Access the website**:
   - Open your web browser
   - Go to: http://127.0.0.1:8000/ or http://localhost:8000/

4. **To stop the server**:
   - Go back to your terminal/command prompt
   - Press `Ctrl+C`

### Step 8: Explore the Admin Interface

1. **Access the admin page**:
   - Go to: http://127.0.0.1:8000/admin/
   - Log in with the superuser credentials you created earlier

2. **Add sample data** to explore the application's features.

### Troubleshooting Common Issues

- **"Python/pip command not found"**: Make sure Python is installed and added to your PATH
- **"No module named..."**: Make sure you've activated the virtual environment and installed dependencies
- **Database errors**: Try deleting `db.sqlite3` file and running `python manage.py migrate` again
- **Can't login to admin**: Run `python manage.py createsuperuser` to create a new admin user

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

## Demo Mode

The application includes a demonstration mode for the payment system. No real payments are processed, and all transactions are simulated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Weather data provided by [Visual Crossing Weather API](https://www.visualcrossing.com/)
- Images from [Unsplash](https://unsplash.com/) 