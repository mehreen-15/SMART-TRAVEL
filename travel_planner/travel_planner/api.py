from django.http import JsonResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test
from users.models import UserActivity, UserProfile
from bookings.models import HotelBooking, Transportation, PaymentTransaction
from destinations.models import Destination

def is_staff(user):
    """Check if user is staff."""
    return user.is_staff

@user_passes_test(is_staff)
def user_activity_data(request):
    """API endpoint for user activity data."""
    # Get activity data for the last 24 hours
    time_threshold = timezone.now() - timedelta(hours=24)
    
    # Get hourly activity counts
    hourly_data = []
    for hour in range(24):
        hour_start = time_threshold + timedelta(hours=hour)
        hour_end = hour_start + timedelta(hours=1)
        
        count = UserActivity.objects.filter(
            timestamp__gte=hour_start,
            timestamp__lt=hour_end
        ).count()
        
        hourly_data.append(count)
    
    # Get recent activity for table
    recent_activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:50]
    
    table_data = []
    for activity in recent_activities:
        table_data.append({
            'username': activity.user.username,
            'action': activity.action,
            'page_visited': activity.page_visited,
            'ip_address': activity.ip_address,
            'timestamp': activity.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': f"{activity.duration:.2f} seconds" if activity.duration else "N/A"
        })
    
    # Generate labels for the last 24 hours
    time_labels = []
    current_hour = timezone.now().hour
    for i in range(24):
        hour = (current_hour - 23 + i) % 24
        time_labels.append(f"{hour}:00")
    
    chart_data = {
        'labels': time_labels,
        'datasets': [{
            'label': 'User Activity',
            'data': hourly_data,
            'borderColor': 'rgba(54, 162, 235, 1)',
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderWidth': 2,
            'fill': True,
            'tension': 0.4
        }]
    }
    
    return JsonResponse({
        'chartData': chart_data,
        'tableData': table_data
    })

@user_passes_test(is_staff)
def booking_data(request):
    """API endpoint for booking data."""
    # Get data for the last 7 days
    time_threshold = timezone.now() - timedelta(days=7)
    
    # Get daily booking counts
    hotel_data = []
    transportation_data = []
    
    for day in range(7):
        day_start = time_threshold + timedelta(days=day)
        day_end = day_start + timedelta(days=1)
        
        hotel_count = HotelBooking.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()
        
        transportation_count = Transportation.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()
        
        hotel_data.append(hotel_count)
        transportation_data.append(transportation_count)
    
    # Get recent bookings for table
    recent_hotel_bookings = HotelBooking.objects.select_related('trip__user', 'hotel').order_by('-created_at')[:25]
    recent_transportation = Transportation.objects.select_related('trip__user').order_by('-created_at')[:25]
    
    table_data = []
    
    for booking in recent_hotel_bookings:
        table_data.append({
            'type': 'Hotel',
            'user': booking.trip.user.username,
            'details': f"{booking.hotel.name} ({booking.room_type})",
            'status': booking.status,
            'date': booking.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': f"${booking.price}"
        })
    
    for booking in recent_transportation:
        table_data.append({
            'type': 'Transportation',
            'user': booking.trip.user.username,
            'details': f"{booking.transportation_type} - {booking.departure_location} to {booking.arrival_location}",
            'status': booking.status,
            'date': booking.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': f"${booking.price}"
        })
    
    # Sort by date
    table_data.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate labels for the last 7 days
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today = timezone.now().weekday()
    
    day_labels = []
    for i in range(7):
        day_index = (today - 6 + i) % 7
        day_labels.append(day_names[day_index])
    
    chart_data = {
        'labels': day_labels,
        'datasets': [
            {
                'label': 'Hotel Bookings',
                'data': hotel_data,
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Transportation Bookings',
                'data': transportation_data,
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    }
    
    return JsonResponse({
        'chartData': chart_data,
        'tableData': table_data[:50]  # Limit to 50 entries
    })

@user_passes_test(is_staff)
def destination_data(request):
    """API endpoint for destination data."""
    # Get the most popular destinations
    popular_destinations = Destination.objects.annotate(
        booking_count=Count('hotel__hotelbooking')
    ).order_by('-booking_count')[:10]
    
    labels = []
    data = []
    
    for destination in popular_destinations:
        labels.append(destination.name)
        data.append(destination.booking_count)
    
    chart_data = {
        'labels': labels,
        'datasets': [{
            'data': data,
            'backgroundColor': [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(199, 199, 199, 0.7)',
                'rgba(83, 102, 255, 0.7)',
                'rgba(40, 159, 64, 0.7)',
                'rgba(210, 199, 199, 0.7)'
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)',
                'rgba(83, 102, 255, 1)',
                'rgba(40, 159, 64, 1)',
                'rgba(210, 199, 199, 1)'
            ],
            'borderWidth': 1
        }]
    }
    
    return JsonResponse({
        'chartData': chart_data
    })

@user_passes_test(is_staff)
def revenue_data(request):
    """API endpoint for revenue data."""
    # Get data for the last 12 months
    today = timezone.now().date()
    start_date = today.replace(day=1) - timedelta(days=365)
    
    monthly_revenue = []
    month_labels = []
    
    for i in range(12):
        month_start = (start_date.replace(day=1) + timedelta(days=32 * i)).replace(day=1)
        if i < 11:
            month_end = (month_start + timedelta(days=32)).replace(day=1)
        else:
            month_end = today + timedelta(days=1)  # Include today
        
        month_revenue = PaymentTransaction.objects.filter(
            timestamp__gte=month_start,
            timestamp__lt=month_end,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_revenue.append(float(month_revenue))
        month_labels.append(month_start.strftime('%b'))
    
    # Get recent payments for table
    recent_payments = PaymentTransaction.objects.select_related('user').order_by('-timestamp')[:50]
    
    table_data = []
    for payment in recent_payments:
        table_data.append({
            'user': payment.user.username,
            'amount': f"${payment.amount}",
            'status': payment.status,
            'method': payment.payment_method,
            'date': payment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_id': payment.transaction_id
        })
    
    chart_data = {
        'labels': month_labels,
        'datasets': [{
            'label': 'Monthly Revenue',
            'data': monthly_revenue,
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderWidth': 2,
            'fill': True,
            'tension': 0.1
        }]
    }
    
    return JsonResponse({
        'chartData': chart_data,
        'tableData': table_data
    }) 