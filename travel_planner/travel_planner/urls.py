"""
URL configuration for travel_planner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from .admin_config import admin_site  # Import the configured admin site
from . import api
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin_site.urls),  # Use our custom admin site
    # path('admin/analytics/', views.analytics_dashboard, name='analytics_dashboard'),  # Real-time analytics dashboard
    # Home page
    path('', TemplateView.as_view(template_name='base/home.html'), name='home'),
    # Static pages
    path('about/', TemplateView.as_view(template_name='base/about.html'), name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
    # App URLs
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('destinations/', include('destinations.urls')),
    path('reviews/', include('reviews.urls')),
    # Auth URLs
    path('login/', views.redirect_to_login, name='login'),
    path('register/', views.redirect_to_register, name='register'),
    path('logout/', views.redirect_to_logout, name='logout'),
    # Redirects for URL compatibility
    path('trips/create/', RedirectView.as_view(pattern_name='bookings:create_trip', permanent=False)),
    path('trips/', RedirectView.as_view(pattern_name='bookings:trip_list', permanent=False)),
    path('accounts/login/', RedirectView.as_view(pattern_name='users:login', permanent=False)),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    # API endpoints
    path('api/analytics/user-activity/', api.user_activity_data, name='api_user_activity'),
    path('api/analytics/bookings/', api.booking_data, name='api_bookings'),
    path('api/analytics/destinations/', api.destination_data, name='api_destinations'),
    path('api/analytics/revenue/', api.revenue_data, name='api_revenue'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
