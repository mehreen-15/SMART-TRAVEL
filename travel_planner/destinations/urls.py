from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list, name='list'),
    path('search/', views.destination_search, name='search'),
    path('attractions/', views.attraction_list, name='attraction_list'),
    path('detail/<int:destination_id>/', views.destination_detail, name='detail'),
    path('accommodations/<int:accommodation_id>/', views.accommodation_detail, name='accommodation_detail'),
    path('attractions/<int:attraction_id>/', views.attraction_detail, name='attraction_detail'),
    path('api/destinations/<int:destination_id>/accommodations/', views.get_accommodations_by_destination, name='api_accommodations'),
    path('api/search-suggestions/', views.search_suggestions, name='api_search_suggestions'),
    path('weather/<int:destination_id>/', views.destination_weather, name='weather'),
    path('api/weather/<str:location>/', views.get_weather_api, name='api_weather'),
] 