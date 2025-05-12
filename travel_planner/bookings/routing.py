from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/booking_updates/$', consumers.BookingUpdatesConsumer.as_asgi()),
] 