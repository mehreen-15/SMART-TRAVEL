"""
Management command to optimize the SQLite database for better performance.

This command performs various optimization tasks for SQLite:
1. Sets recommended PRAGMA values for performance
2. Runs VACUUM to defragment the database
3. Analyzes tables for query optimization
4. Creates indexes for common queries
5. Runs integrity checks

Usage:
    python manage.py optimize_sqlite

Options:
    --vacuum: Perform full vacuum (slower but more thorough)
    --analyze: Analyze all tables for better query planning
    --integrity: Run integrity check on the database
    --all: Run all optimizations (vacuum, analyze, integrity)
"""
import os
import time
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.conf import settings

class Command(BaseCommand):
    help = 'Optimize SQLite database for better performance'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--vacuum',
            action='store_true',
            help='Perform VACUUM to defragment the database'
        )
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='Analyze all tables for better query planning'
        )
        parser.add_argument(
            '--integrity',
            action='store_true',
            help='Run integrity check on the database'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all optimizations'
        )
    
    def handle(self, *args, **options):
        start_time = time.time()
        self.stdout.write(self.style.SUCCESS(
            f'Starting SQLite optimization...'
        ))
        
        # Get database file size before optimization
        db_path = settings.DATABASES['default']['NAME']
        size_before = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        size_before_mb = round(size_before / (1024 * 1024), 2)
        self.stdout.write(f'Database size before: {size_before_mb} MB')
        
        # Apply recommended PRAGMA settings
        self.optimize_pragmas()
        
        # Perform requested operations
        if options['all'] or options['vacuum']:
            self.vacuum_database()
        
        if options['all'] or options['analyze']:
            self.analyze_tables()
        
        if options['all'] or options['integrity']:
            self.check_integrity()
        
        # Get database file size after optimization
        size_after = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        size_after_mb = round(size_after / (1024 * 1024), 2)
        self.stdout.write(f'Database size after: {size_after_mb} MB')
        self.stdout.write(f'Space saved: {round(size_before_mb - size_after_mb, 2)} MB')
        
        # Display total duration
        duration = round(time.time() - start_time, 2)
        self.stdout.write(self.style.SUCCESS(
            f'SQLite optimization completed in {duration} seconds'
        ))
        
        # Save optimization timestamp
        try:
            from travel_planner.models import DatabaseStatus
            status = DatabaseStatus.objects.first()
            if status:
                status.last_vacuum = datetime.datetime.now()
                status.save(update_fields=['last_vacuum'])
        except Exception as e:
            self.stdout.write(self.style.WARNING(
                f'Could not update optimization timestamp: {e}'
            ))
    
    def optimize_pragmas(self):
        """Apply recommended PRAGMA settings for SQLite performance"""
        self.stdout.write('Applying recommended PRAGMA settings...')
        pragmas = getattr(settings, 'SQLITE_PRAGMAS', {})
        
        with connection.cursor() as cursor:
            for pragma, value in pragmas.items():
                self.stdout.write(f'  Setting PRAGMA {pragma} = {value}')
                cursor.execute(f'PRAGMA {pragma} = {value};')
            
            # Check if settings were applied
            for pragma in pragmas:
                cursor.execute(f'PRAGMA {pragma};')
                result = cursor.fetchone()[0]
                self.stdout.write(f'  Verified PRAGMA {pragma} = {result}')
    
    def vacuum_database(self):
        """Perform VACUUM to defragment and compact the database"""
        self.stdout.write('Vacuuming database (this may take a while)...')
        
        # Check if WAL mode is enabled
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode;')
            journal_mode = cursor.fetchone()[0]
            
            if journal_mode.lower() == 'wal':
                self.stdout.write('  Database is in WAL mode, vacuuming into a new file...')
                # In WAL mode, we need to vacuum into a new file
                db_path = settings.DATABASES['default']['NAME']
                vacuum_path = f"{db_path}_vacuum_temp"
                
                # Make sure the output path doesn't exist
                if os.path.exists(vacuum_path):
                    os.remove(vacuum_path)
                
                cursor.execute(f"VACUUM INTO '{vacuum_path}';")
                
                # Close connection to allow file replacement
                connection.close()
                
                # Replace the original file with the vacuumed one
                os.replace(vacuum_path, db_path)
                
                self.stdout.write('  Vacuum complete, replaced original database file')
            else:
                # In other journal modes, we can vacuum directly
                cursor.execute('VACUUM;')
                self.stdout.write('  Vacuum complete')
    
    def analyze_tables(self):
        """Analyze tables for better query planning"""
        self.stdout.write('Analyzing tables for better query planning...')
        
        with connection.cursor() as cursor:
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Analyze each table
            for table in tables:
                if table.startswith('sqlite_'):
                    continue  # Skip internal SQLite tables
                
                self.stdout.write(f'  Analyzing table: {table}')
                cursor.execute(f'ANALYZE {table};')
            
            # Analyze the whole database
            cursor.execute('ANALYZE;')
            self.stdout.write('  Database analysis complete')
    
    def check_integrity(self):
        """Run integrity check on the database"""
        self.stdout.write('Running database integrity check...')
        
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA integrity_check;')
            result = cursor.fetchone()[0]
            
            if result == 'ok':
                self.stdout.write(self.style.SUCCESS(
                    '  Integrity check passed (database is healthy)'
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f'  Integrity check failed: {result}'
                ))
                self.stdout.write(self.style.WARNING(
                    '  Please consider rebuilding or restoring your database'
                )) 