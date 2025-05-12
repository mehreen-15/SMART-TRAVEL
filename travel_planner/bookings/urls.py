from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('create/', views.create_trip, name='create_trip'),
    path('detail/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('edit/<int:trip_id>/', views.edit_trip, name='edit_trip'),
    path('delete/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('<int:trip_id>/itinerary/', views.itinerary, name='itinerary'),
    path('<int:trip_id>/itinerary/add/', views.add_itinerary_item, name='add_itinerary_item'),
    path('<int:trip_id>/transportation/add/', views.add_transportation, name='add_transportation'),
    
    # New booking routes
    path('<int:trip_id>/hotel/book/', views.book_hotel, name='book_hotel'),
    path('<int:trip_id>/transportation/book/', views.book_transportation, name='book_transportation'),
    path('payment/<str:booking_type>/<int:booking_id>/', views.payment, name='payment'),
    
    # E-ticket routes
    path('eticket/<int:ticket_id>/', views.view_eticket, name='view_eticket'),
    path('eticket/<int:ticket_id>/download/', views.download_eticket, name='download_eticket'),
] 