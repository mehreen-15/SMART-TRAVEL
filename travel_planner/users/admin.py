from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, TravelPreference

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# Define inline for TravelPreference
class TravelPreferenceInline(admin.TabularInline):
    model = TravelPreference
    extra = 1
    verbose_name_plural = 'Travel Preferences'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, TravelPreferenceInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login', 'get_phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    date_hierarchy = 'date_joined'
    ordering = ('-date_joined',)
    
    def get_phone(self, obj):
        try:
            return obj.userprofile.phone_number
        except UserProfile.DoesNotExist:
            return ""
    get_phone.short_description = 'Phone Number'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(TravelPreference)
class TravelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget_preference', 'travel_style', 'get_email')
    list_filter = ('budget_preference', 'travel_style')
    search_fields = ('user__username', 'user__email', 'destination_type', 'preferred_activities')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
