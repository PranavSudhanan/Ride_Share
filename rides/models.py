from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('IN_TRANSIT', 'In Transit'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]
    
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rides_as_rider', null=True)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rides_as_driver', null=True)
    
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For ride tracking
    current_location_lat = models.FloatField(null=True)
    current_location_lon = models.FloatField(null=True)
    
    estimated_pickup_time = models.DateTimeField(null=True)
    actual_pickup_time = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)