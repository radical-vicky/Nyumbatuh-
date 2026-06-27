from django.contrib import admin
from .models import PartnershipRequest


@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ['property_name', 'city', 'unit_count', 'contact_name', 'status', 'created_at']
    list_filter = ['status', 'city']
    list_editable = ['status']
    search_fields = ['property_name', 'contact_name', 'contact_email']
