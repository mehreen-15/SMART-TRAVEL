# Smart Travel Planning and Recommendation System

A web-based platform that helps users plan their trips efficiently with personalized recommendations based on user preferences, budget, and real-time travel data.

---

## Windows 10 Setup Guide (No Prior Setup Required)

Follow these steps carefully to avoid common mistakes and ensure a smooth setup.

### 1. Install Python 3.11+
- Download from: https://www.python.org/downloads/windows/
- During installation, **check the box that says "Add Python to PATH"**.

### 2. Install PostgreSQL
- Download from: https://www.postgresql.org/download/windows/
- During installation, **set a password for the `postgres` superuser** (remember this password!).
- Complete the installation and note the version (e.g., 15, 16).

### 3. Add PostgreSQL to System PATH
- Open File Explorer and go to `C:\Program Files\PostgreSQL\<your_version>\bin` (replace `<your_version>` with your installed version).
- Copy this path.
- Press `Win + S`, search for "Environment Variables", and open it.
- Click "Environment Variables..." > In "System variables" select `Path` > Click "Edit..." > Click "New" and paste the path.
- Click OK on all dialogs.
- **Open a new Command Prompt or PowerShell window** for changes to take effect.

### 4. Create the Database
- In the new terminal, run:
  ```sh
  psql -U postgres -c "CREATE DATABASE travel_planner;"
  ```
- If prompted, enter the password you set during PostgreSQL installation.

### 5. Clone the Repository
- Open a terminal and run:
  ```sh
  git clone <repository-url>
  cd travel_planner
  ```

### 6. Create and Activate a Virtual Environment
- In the project root (`C:\Users\<YourName>\Desktop\SMARTTRAVEL`):
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```
- You should see `(venv)` at the start of your prompt.

### 7. Install Python Dependencies
- Run:
  ```sh
  pip install -r requirements.txt
  ```

### 8. Configure Django Database Settings
- Open `travel_planner/travel_planner/settings.py`.
- Ensure the `DATABASES` section looks like this (replace `<your_postgres_password>`):
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'travel_planner',
          'USER': 'postgres',
          'PASSWORD': '<your_postgres_password>',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```

### 9. Run Migrations
- In the `travel_planner` directory:
  ```sh
  python manage.py migrate
  ```

### 10. Create a Superuser
- Run:
  ```sh
  python manage.py createsuperuser
  ```
- Follow the prompts to set up an admin account.

### 11. Run the Development Server
- Run:
  ```sh
  python manage.py runserver
  ```
- Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Common Pitfalls & How to Avoid Them
- **PostgreSQL not in PATH:** If `psql` is not recognized, repeat step 3 and open a new terminal.
- **Wrong database/user/password:** Always use the `postgres` user and the password you set during installation, unless you know how to create/manage other users.
- **Virtual environment not activated:** You must see `(venv)` in your prompt before running Django commands.
- **Forgot to install dependencies:** Always run `pip install -r requirements.txt` after activating your virtual environment.
- **Database does not exist:** Make sure you created the `travel_planner` database with `psql` before running migrations.

---

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

**If you follow these steps exactly, you will avoid all the common mistakes and have your Smart Travel system running smoothly on Windows 10!** 
