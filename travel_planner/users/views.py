from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, TravelPreference
from django import forms

# Custom forms
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                bio="",
                phone_number=""
            )
            
            # Create default travel preferences
            TravelPreference.objects.create(
                user=user,
                destination_type="",
                budget_preference="mid_range",
                travel_style="cultural",
                preferred_activities="",
                dietary_restrictions=""
            )
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next parameter if available, otherwise to home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    travel_preferences = TravelPreference.objects.filter(user=request.user).first()
    return render(request, 'users/profile.html', {
        'user_profile': user_profile,
        'travel_preferences': travel_preferences
    })

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        # Update user details
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        # Update profile
        user_profile.bio = request.POST.get('bio')
        user_profile.phone_number = request.POST.get('phone_number')
        
        # Handle profile picture
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        user_profile.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('users:profile')
    
    return render(request, 'users/edit_profile.html', {'user_profile': user_profile})

@login_required
def preferences(request):
    travel_preferences = TravelPreference.objects.filter(user=request.user).first()
    if not travel_preferences:
        travel_preferences = TravelPreference.objects.create(
            user=request.user,
            destination_type="",
            budget_preference="mid_range",
            travel_style="cultural",
            preferred_activities="",
            dietary_restrictions=""
        )
    return render(request, 'users/preferences.html', {'travel_preferences': travel_preferences})

@login_required
def edit_preferences(request):
    travel_preferences, created = TravelPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        travel_preferences.destination_type = request.POST.get('destination_type')
        travel_preferences.budget_preference = request.POST.get('budget_preference')
        travel_preferences.travel_style = request.POST.get('travel_style')
        travel_preferences.preferred_activities = request.POST.get('preferred_activities')
        travel_preferences.dietary_restrictions = request.POST.get('dietary_restrictions')
        travel_preferences.save()
        
        messages.success(request, 'Your travel preferences have been updated successfully.')
        return redirect('users:preferences')
    
    return render(request, 'users/edit_preferences.html', {'travel_preferences': travel_preferences})
