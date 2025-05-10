import time
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import re
import logging

logger = logging.getLogger('db_performance')

class UserActivityMiddleware:
    """
    Middleware to track user activity and broadcast updates
    through WebSockets for real-time monitoring
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Patterns to ignore in tracking
        self.ignore_patterns = [
            r'^/static/',
            r'^/media/',
            r'^/favicon\.ico$',
            r'^/admin/jsi18n/',
            r'^/__debug__/',
        ]
    
    def __call__(self, request):
        # Start timing the request
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Only track if the setting is enabled
        if not getattr(settings, 'TRACK_USER_ACTIVITY', False):
            return response
        
        # Skip tracking for ignored patterns
        path = request.path
        if any(re.match(pattern, path) for pattern in self.ignore_patterns):
            return response
        
        # Only track authenticated users
        if not request.user.is_authenticated:
            return response
        
        # Calculate request processing time
        processing_time = time.time() - start_time
        
        # Record user activity
        self._record_activity(request, response, processing_time)
        
        return response
    
    def _record_activity(self, request, response, processing_time):
        """Record user activity and send WebSocket updates"""
        user = request.user
        path = request.path
        method = request.method
        status_code = response.status_code
        ip_address = self._get_client_ip(request)
        
        # Update UserProfile if it exists
        try:
            from users.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.last_login = timezone.now()
            profile.last_activity = timezone.now()
            profile.last_ip = ip_address
            profile.save(update_fields=['last_login', 'last_activity', 'last_ip'])
        except:
            pass
        
        # Record to activity log if the model exists
        try:
            from users.models import UserActivity
            UserActivity.objects.create(
                user=user,
                action=f"{method} {path}",
                ip_address=ip_address,
                response_code=status_code,
                processing_time=processing_time,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        except:
            pass
        
        # Only send WebSocket updates for non-admin users or significant actions
        if not (user.is_staff and path.startswith('/admin/')) or status_code >= 400:
            self._send_activity_update(user, path, method, status_code)
    
    def _get_client_ip(self, request):
        """Extract client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
    
    def _send_activity_update(self, user, path, method, status_code):
        """Send activity update through WebSocket channel"""
        try:
            channel_layer = get_channel_layer()
            
            # Send to admin channel
            async_to_sync(channel_layer.group_send)(
                'user_activity',
                {
                    'type': 'user_activity_update',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'path': path,
                        'method': method,
                        'status_code': status_code,
                        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'email': user.email
                    }
                }
            )
        except Exception as e:
            # Just log the error but don't raise an exception
            print(f"Error sending user activity update: {str(e)}")

class DatabasePerformanceMiddleware:
    """
    Middleware to track database performance and query count
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Clear the queries list before the view
        if settings.DEBUG:
            reset_queries = hasattr(connection, 'reset_queries')
            if reset_queries:
                connection.reset_queries()
            
        # Time before the view is called
        start = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Time after the view is called
        duration = time.time() - start
        
        # Log database queries if debug is enabled and there are queries
        if settings.DEBUG and hasattr(connection, 'queries'):
            query_count = len(connection.queries)
            if query_count > 0:
                # Calculate total query time
                query_time = sum(float(q.get('time', 0)) for q in connection.queries)
                
                # Log information about queries
                if query_count > 10 or query_time > 0.5:  # Only log if significant
                    logger.warning(
                        f"Path: {request.path} - {query_count} queries in {query_time:.3f}s "
                        f"(Total request: {duration:.3f}s)"
                    )
                    
                    # Log slow queries
                    for i, query in enumerate(connection.queries):
                        q_time = float(query.get('time', 0))
                        if q_time > 0.1:  # Log queries taking more than 100ms
                            logger.warning(f"Slow query #{i}: {q_time:.3f}s - {query.get('sql', '')}")
        
        return response 