from django.db import models

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations', blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    best_time_to_visit = models.CharField(max_length=100)
    popularity_score = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"

class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
        ('resort', 'Resort'),
        ('villa', 'Villa'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    address = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    amenities = models.TextField()
    image = models.ImageField(upload_to='accommodations', blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.destination.city}"

class Attraction(models.Model):
    CATEGORY_CHOICES = [
        ('nature', 'Nature'),
        ('history', 'Historical'),
        ('culture', 'Cultural'),
        ('entertainment', 'Entertainment'),
        ('food', 'Food & Dining'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opening_hours = models.CharField(max_length=200)
    image = models.ImageField(upload_to='attractions', blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.destination.city}"
