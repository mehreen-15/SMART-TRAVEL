"""Middleware for monitoring and tracking SQLite database connections"""
import uuid
import sqlite3
import datetime
import os
from django.conf import settings
from django.db import connection
from .models import DatabaseConnectionLog, DatabaseStatus

class SQLiteConnectionMiddleware:
    """
    Middleware to track SQLite database connections and performance.
    
    This middleware:
    1. Logs new database connections
    2. Tracks query counts
    3. Updates database status periodically
    4. Provides performance monitoring for SQLite
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize tracker for query counts
        self.query_tracker = {}
        # Generate a connection ID that's unique per middleware instance
        self.connection_id = str(uuid.uuid4())
        # One-time configuration and initialization
        self._update_db_status()
    
    def __call__(self, request):
        # Code to be executed for each request before the view is called
        
        # Generate a connection identifier for this request
        request.db_connection_id = f"{self.connection_id}_{uuid.uuid4().hex[:8]}"
        
        # Store the initial query count for this request
        initial_query_count = len(connection.queries)
        
        # Process the request
        response = self.get_response(request)
        
        # Code to be executed for each request after the view is called
        if settings.DEBUG or getattr(settings, 'DATABASE_STATS_ENABLED', False):
            self._log_connection(request, initial_query_count)
        
        # Periodically update database status (every 50 requests)
        if hasattr(self, '_request_counter'):
            self._request_counter += 1
            if self._request_counter % 50 == 0:
                self._update_db_status()
        else:
            self._request_counter = 1
            
        return response
    
    def _log_connection(self, request, initial_query_count):
        """Log information about the database connection for this request"""
        try:
            # Get current query count
            current_query_count = len(connection.queries)
            query_count = current_query_count - initial_query_count
            
            # Calculate query time
            query_time_ms = sum(
                float(query.get('time', 0)) * 1000  # Convert to milliseconds
                for query in connection.queries[initial_query_count:]
            )
            
            # Get tables accessed (simple parsing, not exhaustive)
            tables_accessed = set()
            for query in connection.queries[initial_query_count:]:
                sql = query.get('sql', '').lower()
                
                # Try to extract table names from FROM and JOIN clauses
                if 'from' in sql:
                    from_parts = sql.split('from')[1].split('where')[0].split(',')
                    for part in from_parts:
                        table = part.strip().split(' ')[0]
                        if table:
                            tables_accessed.add(table)
                            
                if 'join' in sql:
                    join_parts = sql.split('join')
                    for part in join_parts[1:]:
                        table = part.strip().split(' ')[0]
                        if table:
                            tables_accessed.add(table)
            
            # Get SQLite-specific stats
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode;")
            journal_mode = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size;")
            page_size = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA cache_size;")
            cache_size = cursor.fetchone()[0]
            
            # Log the connection data
            log_entry = DatabaseConnectionLog(
                connection_id=request.db_connection_id,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=self._get_client_ip(request),
                query_count=query_count,
                query_time_ms=query_time_ms,
                tables_accessed=','.join(tables_accessed),
                journal_mode=journal_mode,
                page_size=page_size,
                cache_size=cache_size,
                sqlite_version=sqlite3.sqlite_version
            )
            log_entry.save()
            
        except Exception as e:
            # Log the error but don't crash the request
            print(f"Error logging database connection: {e}")
    
    def _update_db_status(self):
        """Update the database status information"""
        try:
            cursor = connection.cursor()
            
            # Get SQLite version
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            
            # Get table count
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
            table_count = cursor.fetchone()[0]
            
            # Get index count
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index';")
            index_count = cursor.fetchone()[0]
            
            # Get database size
            db_path = settings.DATABASES['default']['NAME']
            size_bytes = os.path.getsize(db_path) if os.path.exists(db_path) else 0
            
            # Get SQLite configuration
            cursor.execute("PRAGMA journal_mode;")
            journal_mode = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA synchronous;")
            synchronous = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA cache_size;")
            cache_size = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size;")
            page_size = cursor.fetchone()[0]
            
            # Get integrity check
            cursor.execute("PRAGMA quick_check;")
            integrity_check = cursor.fetchone()[0]
            
            # Try to get last vacuum time (not always available)
            last_vacuum = None
            try:
                cursor.execute("PRAGMA last_vacuum;")
                vacuum_result = cursor.fetchone()
                if vacuum_result and vacuum_result[0]:
                    last_vacuum = datetime.datetime.fromtimestamp(vacuum_result[0])
            except:
                pass
            
            # Update or create database status
            status, created = DatabaseStatus.objects.get_or_create(
                defaults={
                    'version': version,
                    'size_bytes': size_bytes,
                    'table_count': table_count,
                    'index_count': index_count,
                    'journal_mode': journal_mode,
                    'synchronous_setting': synchronous,
                    'cache_size': cache_size, 
                    'page_size': page_size,
                    'last_vacuum': last_vacuum,
                    'integrity_check': integrity_check
                }
            )
            
            if not created:
                status.version = version
                status.size_bytes = size_bytes
                status.table_count = table_count
                status.index_count = index_count
                status.journal_mode = journal_mode
                status.synchronous_setting = synchronous
                status.cache_size = cache_size
                status.page_size = page_size
                if last_vacuum:
                    status.last_vacuum = last_vacuum
                status.integrity_check = integrity_check
                status.save()
                
        except Exception as e:
            # Log the error but don't crash
            print(f"Error updating database status: {e}")
    
    def _get_client_ip(self, request):
        """Get the client IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 