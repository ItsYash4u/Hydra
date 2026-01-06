from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None  # 🔴 IMPORTANT: removes username field

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(_("email address"), unique=True)

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    station_name = models.CharField(_("Station Name"), blank=True, max_length=255, default="")
    user_type = models.CharField(_("Type of User"), blank=True, max_length=50, default="")
    phone_number = models.CharField(_("Phone Number"), max_length=15, unique=True, null=True, blank=True)
    age = models.IntegerField(_("Age"), null=True, blank=True)
    
    # Role field for user/admin access control
    role = models.CharField(_("Role"), max_length=10, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin' or self.is_staff or self.is_superuser


class OTP(models.Model):
    """
    One-Time Password for email/phone verification.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from django.utils import timezone
        # Valid for 10 minutes
        return (
            not self.is_used 
            and (timezone.now() - self.created_at).total_seconds() < 600
        )

    def __str__(self):
        return f"OTP for {self.user.email}"