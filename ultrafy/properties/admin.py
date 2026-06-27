from django.contrib import admin
from .models import Property, PropertyImage, PropertyAmenity, PropertyInquiry


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 2


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'city', 'status', 'ultrafy_partner', 'is_featured', 'is_active', 'created_at']
    list_filter = ['property_type', 'status', 'ultrafy_partner', 'is_featured', 'is_active', 'city']
    search_fields = ['title', 'address', 'city', 'owner__email']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline, PropertyAmenityInline]
    list_editable = ['is_featured', 'ultrafy_partner', 'is_active']


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'property', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
