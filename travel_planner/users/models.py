from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class TravelPreference(models.Model):
    BUDGET_CHOICES = [
        ('budget', 'Budget'),
        ('mid_range', 'Mid-Range'),
        ('luxury', 'Luxury'),
    ]
    
    TRAVEL_STYLE_CHOICES = [
        ('adventure', 'Adventure'),
        ('relaxation', 'Relaxation'),
        ('cultural', 'Cultural'),
        ('food', 'Food & Culinary'),
        ('eco', 'Eco-friendly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_type = models.CharField(max_length=100)
    budget_preference = models.CharField(max_length=10, choices=BUDGET_CHOICES)
    travel_style = models.CharField(max_length=10, choices=TRAVEL_STYLE_CHOICES)
    preferred_activities = models.TextField()
    dietary_restrictions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Travel Preferences"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    page_visited = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(blank=True, null=True)  # Duration in seconds
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
    
    class Meta:
        verbose_name_plural = "User Activities"
