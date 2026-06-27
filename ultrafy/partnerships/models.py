from django.db import models
from django.contrib.auth.models import User
import uuid


class PartnershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Not Approved'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnership_requests')
    property_name = models.CharField(max_length=200)
    property_address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    unit_count = models.PositiveIntegerField()
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=30)
    contact_email = models.EmailField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Partnership: {self.property_name} — {self.get_status_display()}"
