from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination, Accommodation, Attraction

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class DestinationReview(Review):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    weather_rating = models.PositiveSmallIntegerField()  # 1-5 stars
    safety_rating = models.PositiveSmallIntegerField()  # 1-5 stars
    
    def __str__(self):
        return f"Review for {self.destination.name} by {self.user.username}"

class AccommodationReview(Review):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reviews')
    cleanliness_rating = models.PositiveSmallIntegerField()  # 1-5 stars
    service_rating = models.PositiveSmallIntegerField()  # 1-5 stars
    value_rating = models.PositiveSmallIntegerField()  # 1-5 stars
    
    def __str__(self):
        return f"Review for {self.accommodation.name} by {self.user.username}"

class AttractionReview(Review):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='reviews')
    value_for_money = models.PositiveSmallIntegerField()  # 1-5 stars
    
    def __str__(self):
        return f"Review for {self.attraction.name} by {self.user.username}"
