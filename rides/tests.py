import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ride
from .serializers import RideSerializer

class TestRideViewSet(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='test@example.com'
        )
        self.driver = get_user_model().objects.create_user(
            username='testdriver',
            password='password123',
            email='driver@example.com'
        )
        self.driver.is_driver = True
        self.driver.save()
        
        # Create token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Create a test ride
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="Test Location",
            dropoff_location="Destination",
            status="REQUESTED"
        )

    def test_rider_can_create_ride(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.post(reverse('ride-list'), {
            'pickup_location': 'Start Point',
            'dropoff_location': 'End Point'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 2)
        
        ride_data = json.loads(response.content)
        self.assertEqual(ride_data['rider'], self.user.id)

class TestRideStatusUpdateViewSet(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='test@example.com'
        )
        self.driver = get_user_model().objects.create_user(
            username='testdriver',
            password='password123',
            email='driver@example.com'
        )
        self.driver.is_driver = True
        self.driver.save()
        
        # Create token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Create a test ride
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="Test Location",
            dropoff_location="Destination",
            status="REQUESTED"
        )

    def test_driver_can_update_status(self):
        refresh = RefreshToken.for_user(self.driver)
        driver_access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {driver_access_token}')
        
        url = reverse('ride-status-detail', kwargs={'pk': self.ride.pk})
        
        response = self.client.patch(url, {'status': 'ACCEPTED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_ride = Ride.objects.get(pk=self.ride.pk)
        self.assertEqual(updated_ride.status, 'ACCEPTED')

class TestRideTrackingViewSet(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='test@example.com'
        )
        self.driver = get_user_model().objects.create_user(
            username='testdriver',
            password='password123',
            email='driver@example.com'
        )
        self.driver.is_driver = True
        self.driver.save()
        
        # Create token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Create a test ride
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="Test Location",
            dropoff_location="Destination",
            status="REQUESTED"
        )

    def test_driver_can_update_location(self):
        refresh = RefreshToken.for_user(self.driver)
        driver_access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {driver_access_token}')
        
        url = reverse('ride-tracking-detail', kwargs={'pk': self.ride.pk})
        
        response = self.client.patch(url, {
            'latitude': 37.7749,
            'longitude': -122.4194
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_ride = Ride.objects.get(pk=self.ride.pk)
        self.assertAlmostEqual(updated_ride.current_location_lat, 37.7749)
        self.assertAlmostEqual(updated_ride.current_location_lon, -122.4194)