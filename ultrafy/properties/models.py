from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class PropertyType(models.TextChoices):
    APARTMENT = 'apartment', 'Apartment'
    OFFICE = 'office', 'Office Space'
    COMMERCIAL = 'commercial', 'Commercial Space'
    BUILDING = 'building', 'Entire Building'
    CONDO = 'condo', 'Condominium'


class ListingStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    PARTIALLY_OCCUPIED = 'partial', 'Partially Occupied'
    OCCUPIED = 'occupied', 'Fully Occupied'
    COMING_SOON = 'coming_soon', 'Coming Soon'


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.AVAILABLE)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Philippines')
    total_units = models.PositiveIntegerField(default=1)
    available_units = models.PositiveIntegerField(default=1)
    floor_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_for_sale = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    is_for_rent = models.BooleanField(default=True)
    is_for_sale = models.BooleanField(default=False)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    floors = models.PositiveIntegerField(null=True, blank=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    # Ultrafy Partnership
    ultrafy_partner = models.BooleanField(default=False)
    internet_speed_mbps = models.PositiveIntegerField(null=True, blank=True)

    # Featured
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state_province}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} — {self.property.title}"


class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    inquirer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} on {self.property.title}"
