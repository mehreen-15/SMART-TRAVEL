from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DestinationReview, AccommodationReview, AttractionReview
from destinations.models import Destination, Accommodation, Attraction
from .forms import DestinationReviewForm, AccommodationReviewForm, AttractionReviewForm

@login_required
def review_list(request):
    destination_reviews = DestinationReview.objects.filter(user=request.user)
    accommodation_reviews = AccommodationReview.objects.filter(user=request.user)
    attraction_reviews = AttractionReview.objects.filter(user=request.user)
    return render(request, 'reviews/list.html', {
        'destination_reviews': destination_reviews,
        'accommodation_reviews': accommodation_reviews,
        'attraction_reviews': attraction_reviews
    })

@login_required
def add_destination_review(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    
    # Check if user already reviewed this destination
    existing_review = DestinationReview.objects.filter(user=request.user, destination=destination).first()
    if existing_review:
        messages.info(request, f"You've already reviewed {destination.name}. You can edit your review.")
        return redirect('reviews:edit_review', review_id=existing_review.id)
    
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.created_at = timezone.now()
            review.save()
            messages.success(request, f"Thank you for reviewing {destination.name}!")
            return redirect('destinations:detail', destination_id=destination.id)
    else:
        form = DestinationReviewForm()
        
    return render(request, 'reviews/add_destination_review.html', {
        'form': form,
        'destination': destination
    })

@login_required
def add_accommodation_review(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    
    # Check if user already reviewed this accommodation
    existing_review = AccommodationReview.objects.filter(user=request.user, accommodation=accommodation).first()
    if existing_review:
        messages.info(request, f"You've already reviewed {accommodation.name}. You can edit your review.")
        return redirect('reviews:edit_review', review_id=existing_review.id)
    
    if request.method == 'POST':
        form = AccommodationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.accommodation = accommodation
            review.created_at = timezone.now()
            review.save()
            messages.success(request, f"Thank you for reviewing {accommodation.name}!")
            return redirect('destinations:accommodation_detail', accommodation_id=accommodation.id)
    else:
        form = AccommodationReviewForm()
        
    return render(request, 'reviews/add_accommodation_review.html', {
        'form': form,
        'accommodation': accommodation
    })

@login_required
def add_attraction_review(request, attraction_id):
    attraction = get_object_or_404(Attraction, pk=attraction_id)
    
    # Check if user already reviewed this attraction
    existing_review = AttractionReview.objects.filter(user=request.user, attraction=attraction).first()
    if existing_review:
        messages.info(request, f"You've already reviewed {attraction.name}. You can edit your review.")
        return redirect('reviews:edit_review', review_id=existing_review.id)
    
    if request.method == 'POST':
        form = AttractionReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.attraction = attraction
            review.created_at = timezone.now()
            review.save()
            messages.success(request, f"Thank you for reviewing {attraction.name}!")
            return redirect('destinations:attraction_detail', attraction_id=attraction.id)
    else:
        form = AttractionReviewForm()
        
    return render(request, 'reviews/add_attraction_review.html', {
        'form': form,
        'attraction': attraction
    })

@login_required
def edit_review(request, review_id):
    # Determine the review type and get the appropriate object
    review = None
    review_type = None
    
    try:
        review = DestinationReview.objects.get(id=review_id, user=request.user)
        review_type = 'destination'
        form_class = DestinationReviewForm
        redirect_url = ('destinations:detail', review.destination.id)
    except DestinationReview.DoesNotExist:
        try:
            review = AccommodationReview.objects.get(id=review_id, user=request.user)
            review_type = 'accommodation'
            form_class = AccommodationReviewForm
            redirect_url = ('destinations:accommodation_detail', review.accommodation.id)
        except AccommodationReview.DoesNotExist:
            try:
                review = AttractionReview.objects.get(id=review_id, user=request.user)
                review_type = 'attraction'
                form_class = AttractionReviewForm
                redirect_url = ('destinations:attraction_detail', review.attraction.id)
            except AttractionReview.DoesNotExist:
                messages.error(request, "Review not found.")
                return redirect('reviews:list')
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated!")
            return redirect(redirect_url[0], redirect_url[1])
    else:
        form = form_class(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review,
        'review_type': review_type
    })

@login_required
def delete_review(request, review_id):
    # Determine the review type and get the appropriate object
    review = None
    redirect_url = None
    
    try:
        review = DestinationReview.objects.get(id=review_id, user=request.user)
        redirect_url = ('destinations:detail', review.destination.id)
    except DestinationReview.DoesNotExist:
        try:
            review = AccommodationReview.objects.get(id=review_id, user=request.user)
            redirect_url = ('destinations:accommodation_detail', review.accommodation.id)
        except AccommodationReview.DoesNotExist:
            try:
                review = AttractionReview.objects.get(id=review_id, user=request.user)
                redirect_url = ('destinations:attraction_detail', review.attraction.id)
            except AttractionReview.DoesNotExist:
                messages.error(request, "Review not found.")
                return redirect('reviews:list')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect(redirect_url[0], redirect_url[1])
    
    return render(request, 'reviews/delete_review.html', {'review': review})
