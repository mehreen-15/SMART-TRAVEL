import datetime
import json
from django.utils import timezone
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # Get the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        # Set the start time
        request.start_time = timezone.now()
        
        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        
        # Skip certain paths
        if any(path in request.path for path in ['/static/', '/media/', '/admin/jsi18n/']):
            return response
            
        # Only track activity for authenticated users
        if request.user.is_authenticated:
            # Calculate request duration
            duration = timezone.now() - request.start_time
            
            # Log user activity
            activity = UserActivity.objects.create(
                user=request.user,
                action=request.method,
                ip_address=ip,
                page_visited=request.path,
                timestamp=timezone.now(),
                duration=duration.total_seconds()
            )
            
            # Send to WebSocket group if enabled
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'user_activity',
                    {
                        'type': 'user_activity_message',
                        'message': {
                            'user_id': request.user.id,
                            'username': request.user.username,
                            'action': request.method,
                            'page': request.path,
                            'timestamp': timezone.now().isoformat(),
                            'ip': ip,
                            'duration': duration.total_seconds()
                        }
                    }
                )
            except Exception as e:
                # Log the error but don't break the request
                print(f"Error sending to WebSocket: {e}")
                
        return response 