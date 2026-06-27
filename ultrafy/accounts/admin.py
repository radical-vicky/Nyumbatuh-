from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_partner', 'phone', 'created_at']
    list_filter = ['role', 'is_partner']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
