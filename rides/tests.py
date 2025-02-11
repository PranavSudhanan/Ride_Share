# from django.test import TestCase
# from rest_framework.test import APITestCase
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# from .models import Ride

# class RideModelTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='password123'
#         )
    
#     def test_ride_creation(self):
#         ride = Ride.objects.create(
#             rider=self.user,
#             pickup_location="Test Location",
#             dropoff_location="Destination"
#         )
        
#         self.assertEqual(ride.rider, self.user)
#         self.assertEqual(ride.status, 'REQUESTED')

# class RideAPITests(APITestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='password123'
#         )
#         token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
#     def test_create_ride(self):
#         response = self.client.post('/rides/', {
#             'pickup_location': 'Test Location',
#             'dropoff_location': 'Destination'
#         })
        
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Ride.objects.count(), 1)