from django import forms
from .models import DestinationReview, AccommodationReview, AttractionReview

class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['rating', 'weather_rating', 'safety_rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'},
                                  choices=[(i, i) for i in range(1, 6)]),
            'weather_rating': forms.Select(attrs={'class': 'form-select'},
                                         choices=[(i, i) for i in range(1, 6)]),
            'safety_rating': forms.Select(attrs={'class': 'form-select'},
                                        choices=[(i, i) for i in range(1, 6)])
        }
        labels = {
            'rating': 'Overall Rating (1-5)',
            'weather_rating': 'Weather Experience (1-5)',
            'safety_rating': 'Safety Rating (1-5)',
            'comment': 'Your Experience'
        }

class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['rating', 'cleanliness_rating', 'service_rating', 'value_rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'},
                                  choices=[(i, i) for i in range(1, 6)]),
            'cleanliness_rating': forms.Select(attrs={'class': 'form-select'},
                                             choices=[(i, i) for i in range(1, 6)]),
            'service_rating': forms.Select(attrs={'class': 'form-select'},
                                         choices=[(i, i) for i in range(1, 6)]),
            'value_rating': forms.Select(attrs={'class': 'form-select'},
                                       choices=[(i, i) for i in range(1, 6)])
        }
        labels = {
            'rating': 'Overall Rating (1-5)',
            'cleanliness_rating': 'Cleanliness (1-5)',
            'service_rating': 'Service Quality (1-5)',
            'value_rating': 'Value for Money (1-5)',
            'comment': 'Your Experience'
        }

class AttractionReviewForm(forms.ModelForm):
    class Meta:
        model = AttractionReview
        fields = ['rating', 'value_for_money', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'},
                                  choices=[(i, i) for i in range(1, 6)]),
            'value_for_money': forms.Select(attrs={'class': 'form-select'},
                                          choices=[(i, i) for i in range(1, 6)])
        }
        labels = {
            'rating': 'Overall Rating (1-5)',
            'value_for_money': 'Value for Money (1-5)',
            'comment': 'Your Experience'
        } 