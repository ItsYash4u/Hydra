from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
# from .models import SensorReading, Alert, AlertRule, UserRole
# Models SensorReading, Alert, AlertRule, UserRole are missing in models.py.
# Commenting out signals to prevent crash.

import logging

logger = logging.getLogger(__name__)


# @receiver(post_save, sender=User)
# def create_user_role(sender, instance, created, **kwargs):
#     """Auto-create UserRole when a new user is created"""
#     if created:
#         # UserRole model is missing.
#         # UserRole.objects.get_or_create(
#         #     user=instance,
#         #     defaults={'role': 'farm_operator'}
#         # )
#         logger.info(f'UserRole creation skipped for {instance.username}')


# @receiver(post_save, sender=SensorReading)
# def check_alert_thresholds(sender, instance, created, **kwargs):
#     ... (commented out due to missing models) ...

def ready():
    """Import signals when app is ready"""
    pass

