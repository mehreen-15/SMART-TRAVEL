"""
Custom application configuration for Travel Planner.
Sets up SQLite optimizations on startup.
"""
from django.apps import AppConfig
from django.db import connection
from django.conf import settings


class TravelPlannerConfig(AppConfig):
    """
    Travel Planner application configuration.
    Sets up SQLite optimizations and database performance monitoring.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel_planner'

    def ready(self):
        """
        Apply SQLite optimizations on application startup.
        This method is called when the application is ready to process requests.
        """
        # Only apply optimizations if we're using SQLite
        if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            self.apply_sqlite_optimizations()
            self.register_connection_signals()
    
    def apply_sqlite_optimizations(self):
        """Apply SQLite performance optimizations from settings"""
        try:
            pragmas = getattr(settings, 'SQLITE_PRAGMAS', {})
            if not pragmas:
                return
                
            with connection.cursor() as cursor:
                # Apply each PRAGMA setting from the configuration
                for pragma, value in pragmas.items():
                    cursor.execute(f"PRAGMA {pragma} = {value};")
                
                # Verify the settings were applied
                for pragma in pragmas:
                    cursor.execute(f"PRAGMA {pragma};")
                    result = cursor.fetchone()[0]
                    print(f"SQLite optimizer: PRAGMA {pragma} = {result}")
                
                print("SQLite optimizations applied successfully")
                
        except Exception as e:
            print(f"Error applying SQLite optimizations: {e}")
    
    def register_connection_signals(self):
        """Register connection-related signals"""
        # Import here to avoid circular imports
        from django.db.backends.signals import connection_created
        
        # Define connection created handler
        def optimize_sqlite_connection(sender, connection, **kwargs):
            """Handler for new database connections"""
            if 'sqlite3' in connection.vendor:
                # Apply per-connection optimizations
                with connection.cursor() as cursor:
                    # Enable foreign key constraints for this connection
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    
                    # Optimize memory usage
                    cursor.execute("PRAGMA temp_store = MEMORY;")
                    
                    # Set cache size
                    cursor.execute("PRAGMA cache_size = -10000;")  # 10MB cache
        
        # Connect the signal
        connection_created.connect(optimize_sqlite_connection) 