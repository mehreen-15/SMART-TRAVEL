"""
Context processors for the Travel Planner application.
Provides database information to templates.
"""
import sqlite3
import os
from django.conf import settings
from django.db import connection
import datetime

def database_info(request):
    """
    Provide database connection information for display in templates.
    Retrieves SQLite database metadata and statistics.
    """
    database_stats = {
        'engine': 'SQLite',
        'db_name': os.path.basename(settings.DATABASES['default']['NAME']),
        'version': sqlite3.sqlite_version,
        'size': _get_db_size(),
        'tables': _get_tables_count(),
        'connection_age': _get_connection_age(),
        'active_connections': _get_active_connections(),
        'last_vacuum': _get_last_vacuum(),
        'pooling_enabled': getattr(settings, 'DATABASE_CONNECTION_POOLING', False),
        'max_connections': getattr(settings, 'MAX_CONNECTIONS', 0),
    }
    
    return {'database_stats': database_stats}

def _get_db_size():
    """Get the database file size in MB."""
    db_path = settings.DATABASES['default']['NAME']
    try:
        size_bytes = os.path.getsize(db_path)
        return round(size_bytes / (1024 * 1024), 2)  # Convert to MB
    except (OSError, FileNotFoundError):
        return 0

def _get_tables_count():
    """Get the number of tables in the database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            return cursor.fetchone()[0]
    except Exception:
        return 0

def _get_connection_age():
    """Get the age of the current database connection."""
    if hasattr(connection, 'connection_created_time'):
        age = datetime.datetime.now() - connection.connection_created_time
        return round(age.total_seconds())
    else:
        # Set connection creation time if not already set
        connection.connection_created_time = datetime.datetime.now()
        return 0

def _get_active_connections():
    """
    Get the number of active connections.
    For SQLite, this is usually 1 as it doesn't support multiple connections.
    """
    return 1  # SQLite typically has only one connection

def _get_last_vacuum():
    """Get the timestamp of the last VACUUM operation."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA last_vacuum;")
            timestamp = cursor.fetchone()[0]
            if timestamp:
                return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        pass
    return 'Unknown' 