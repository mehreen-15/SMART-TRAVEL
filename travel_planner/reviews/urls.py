from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='list'),
    path('destination/<int:destination_id>/add/', views.add_destination_review, name='add_destination_review'),
    path('accommodation/<int:accommodation_id>/add/', views.add_accommodation_review, name='add_accommodation_review'),
    path('attraction/<int:attraction_id>/add/', views.add_attraction_review, name='add_attraction_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
] 