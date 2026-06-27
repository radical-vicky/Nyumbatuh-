from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('tenant', 'Tenant / Buyer'),
        ('owner', 'Property Owner'),
        ('developer', 'Developer'),
        ('business', 'Business Owner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_partner = models.BooleanField(default=False)
    partner_since = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.get_role_display()})"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.email.split('@')[0]
