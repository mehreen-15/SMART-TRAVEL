from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.db import connection
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

# Import your models
from users.models import UserProfile, TravelPreference
from destinations.models import Destination, Accommodation, Attraction
from bookings.models import Trip, HotelBooking, TransportationBooking, PaymentTransaction, ETicket
from .models import DatabaseConnectionLog, DatabaseStatus

class TravelPlannerAdminSite(AdminSite):
    site_header = "Smart Travel Admin"
    site_title = "Smart Travel Admin Portal"
    index_title = "Welcome to Smart Travel Admin Portal"
    
    # Custom admin colors
    admin_color_primary = "#1976d2"
    admin_color_secondary = "#6c757d"
    admin_color_accent = "#28a745"
    
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request)
        
        # Sort the apps alphabetically
        app_list.sort(key=lambda x: x['name'].lower())
        
        # Sort the models alphabetically within each app
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
            
        return app_list
    
    def index(self, request, extra_context=None):
        """
        Customize the admin index page with statistics and quick access links
        """
        # Count various model instances
        stats = {
            'users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'destinations': Destination.objects.count(),
            'accommodations': Accommodation.objects.count(),
            'attractions': Attraction.objects.count(),
            'trips': Trip.objects.count(),
            'hotel_bookings': HotelBooking.objects.count(),
            'transportation_bookings': TransportationBooking.objects.count(),
            'payment_transactions': PaymentTransaction.objects.count(),
            'tickets': ETicket.objects.count(),
        }
        
        # Get total revenue
        total_revenue = PaymentTransaction.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Get most popular destinations (top 5)
        popular_destinations = Destination.objects.order_by('-popularity_score')[:5]
        
        # Get recent bookings (last 5)
        recent_hotel_bookings = HotelBooking.objects.order_by('-booking_date')[:5]
        recent_transportation_bookings = TransportationBooking.objects.order_by('-booking_date')[:5]
        
        # Get recent payments (last 5)
        recent_payments = PaymentTransaction.objects.order_by('-created_at')[:5]
        
        # Get database performance statistics
        db_stats = self.get_database_stats()
        
        # Generate quick links using direct paths rather than URL reversals
        quick_links = [
            {
                'name': 'Users',
                'link': '/admin/auth/user/',
                'icon': 'fas fa-users',
                'color': '#1976d2'  # Primary blue
            },
            {
                'name': 'Destinations',
                'link': '/admin/destinations/destination/',
                'icon': 'fas fa-map-marker-alt',
                'color': '#28a745'  # Success green
            },
            {
                'name': 'Trips',
                'link': '/admin/bookings/trip/',
                'icon': 'fas fa-suitcase',
                'color': '#6f42c1'  # Purple
            },
            {
                'name': 'Hotel Bookings',
                'link': '/admin/bookings/hotelbooking/',
                'icon': 'fas fa-hotel',
                'color': '#fd7e14'  # Orange
            },
            {
                'name': 'Transportation',
                'link': '/admin/bookings/transportation/',
                'icon': 'fas fa-plane',
                'color': '#e83e8c'  # Pink
            },
            {
                'name': 'Payments',
                'link': '/admin/bookings/paymenttransaction/',
                'icon': 'fas fa-credit-card',
                'color': '#20c997'  # Teal
            },
            {
                'name': 'E-Tickets',
                'link': '/admin/bookings/eticket/',
                'icon': 'fas fa-ticket-alt',
                'color': '#fd7e14'  # Orange
            },
            {
                'name': 'Attractions',
                'link': '/admin/destinations/attraction/',
                'icon': 'fas fa-landmark',
                'color': '#17a2b8'  # Info blue
            },
            {
                'name': 'Database Stats',
                'link': '/admin/travel_planner/databasestatus/',
                'icon': 'fas fa-database',
                'color': '#6c757d'  # Secondary gray
            }
        ]
        
        context = {
            'stats': stats,
            'total_revenue': total_revenue,
            'popular_destinations': popular_destinations,
            'recent_hotel_bookings': recent_hotel_bookings,
            'recent_transportation_bookings': recent_transportation_bookings,
            'recent_payments': recent_payments,
            'quick_links': quick_links,
            'db_stats': db_stats,
            **super().index(request, extra_context=extra_context).context_data,
        }
        
        # Add the admin dashboard css
        extra_css = """
        <style>
            .dashboard-stats {
                display: flex;
                flex-wrap: wrap;
                margin-bottom: 20px;
            }
            .stat-box {
                background-color: #fff;
                border-radius: 8px;
                padding: 20px;
                margin-right: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                min-width: 200px;
                flex: 1;
            }
            .stat-value {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .stat-label {
                color: #777;
                font-size: 14px;
            }
            .dashboard-section {
                margin-bottom: 30px;
            }
            .dashboard-section h2 {
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 1px solid #eee;
            }
            .quick-links {
                display: flex;
                flex-wrap: wrap;
                margin-bottom: 20px;
            }
            .quick-link {
                display: flex;
                align-items: center;
                background-color: #fff;
                border-radius: 8px;
                padding: 15px;
                margin-right: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-decoration: none;
                color: #333;
                min-width: 200px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .quick-link:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .quick-link-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 10px;
                color: #fff;
            }
            .quick-link-text {
                font-weight: 500;
            }
            .recent-item {
                padding: 10px 15px;
                border-bottom: 1px solid #eee;
            }
            .recent-item:last-child {
                border-bottom: none;
            }
            .recent-item a {
                text-decoration: none;
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 20px;
            }
            .dashboard-card {
                background-color: #fff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            @media (max-width: 1200px) {
                .dashboard-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """
        context['extra_style'] = extra_css
        
        return super().index(request, extra_context=context)
    
    def get_database_stats(self):
        """Get SQLite database statistics"""
        try:
            with connection.cursor() as cursor:
                # Get SQLite version
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                
                # Get table count
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
                table_count = cursor.fetchone()[0]
                
                # Get database size
                cursor.execute("PRAGMA page_count;")
                page_count = cursor.fetchone()[0]
                cursor.execute("PRAGMA page_size;")
                page_size = cursor.fetchone()[0]
                size_mb = round((page_count * page_size) / (1024 * 1024), 2)
                
                # Get SQLite configuration
                cursor.execute("PRAGMA journal_mode;")
                journal_mode = cursor.fetchone()[0]
                
                cursor.execute("PRAGMA synchronous;")
                synchronous = cursor.fetchone()[0]
                
                cursor.execute("PRAGMA cache_size;")
                cache_size = cursor.fetchone()[0]
                
                # Get query statistics
                cursor.execute("PRAGMA query_stats;")
                query_stats = cursor.fetchone()
                queries_executed = query_stats[0] if query_stats else 'N/A'
                
                # Get performance recommendations
                recommendations = []
                cursor.execute("PRAGMA integrity_check;")
                integrity = cursor.fetchone()[0]
                if integrity != 'ok':
                    recommendations.append("Database integrity issues detected")
                
                if journal_mode.lower() != 'wal':
                    recommendations.append("Consider using WAL journal mode for better performance")
                
                if synchronous > 1:
                    recommendations.append("Consider reducing synchronous level for better performance")
                
                return {
                    'engine': 'SQLite',
                    'version': version,
                    'tables': table_count,
                    'size_mb': size_mb,
                    'journal_mode': journal_mode,
                    'synchronous': synchronous,
                    'cache_size': cache_size,
                    'queries_executed': queries_executed,
                    'recommendations': recommendations,
                    'connection_string': 'sqlite:///' + str(connection.settings_dict['NAME'])
                }
        except Exception as e:
            return {
                'engine': 'SQLite',
                'error': str(e),
                'connection_string': 'sqlite:///' + str(connection.settings_dict['NAME'])
            }

# Instantiate the custom admin site
admin_site = TravelPlannerAdminSite(name='smarttravel_admin')

# Register the database models with the admin site
class DatabaseStatusAdmin(admin.ModelAdmin):
    list_display = ('engine', 'version', 'size_mb', 'table_count', 'journal_mode', 'health_status', 'last_update')
    readonly_fields = ('engine', 'version', 'size_bytes', 'table_count', 'index_count', 'journal_mode', 
                      'synchronous_setting', 'cache_size', 'page_size', 'last_vacuum', 'integrity_check', 'last_update')
    
    fieldsets = (
        ('Database Information', {
            'fields': ('engine', 'version', 'size_bytes', 'table_count', 'index_count', 'last_update')
        }),
        ('Configuration', {
            'fields': ('journal_mode', 'synchronous_setting', 'cache_size', 'page_size')
        }),
        ('Health', {
            'fields': ('last_vacuum', 'integrity_check')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manually adding database status entries
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting database status entries
        return False

class DatabaseConnectionLogAdmin(admin.ModelAdmin):
    list_display = ('connection_id', 'timestamp', 'ip_address', 'query_count', 'query_time_ms', 'avg_query_time')
    list_filter = ('timestamp', 'journal_mode')
    search_fields = ('connection_id', 'ip_address', 'user_agent', 'tables_accessed')
    readonly_fields = ('connection_id', 'timestamp', 'user_agent', 'ip_address', 'query_count', 'query_time_ms',
                      'tables_accessed', 'journal_mode', 'page_size', 'cache_size', 'sqlite_version', 'connection_duration')
    
    fieldsets = (
        ('Connection Information', {
            'fields': ('connection_id', 'timestamp', 'user_agent', 'ip_address')
        }),
        ('Query Statistics', {
            'fields': ('query_count', 'query_time_ms', 'tables_accessed')
        }),
        ('SQLite Configuration', {
            'fields': ('journal_mode', 'page_size', 'cache_size', 'sqlite_version')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manually adding connection logs
        return False

# Register the models with the admin site
admin_site.register(DatabaseStatus, DatabaseStatusAdmin)
admin_site.register(DatabaseConnectionLog, DatabaseConnectionLogAdmin) 