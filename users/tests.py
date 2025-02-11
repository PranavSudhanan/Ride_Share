from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

class CustomUserModelTests(TestCase):
    def setUp(self):
        # Use different usernames to avoid conflicts
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            password='password123'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='password123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertTrue(self.user1.is_active)
        self.assertFalse(self.user1.is_driver)
        self.assertFalse(self.user1.is_staff)
        self.assertFalse(self.user1.is_superuser)
    
    def test_custom_related_names(self):
        # Test custom related names don't clash with auth.User
        group = self.user1.groups.create(name='Test Group')
        
        # Check custom related names work
        self.assertEqual(group.custom_user_set.count(), 1)
        self.assertEqual(group.custom_user_set.first(), self.user1)

class UserRegisterViewSetTests(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin1',
            password='adminpassword'
        )
        self.normal_user = get_user_model().objects.create_user(
            username='normal1',
            password='normalpassword'
        )
        self.admin_client = APIClient()
        self.normal_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        self.normal_client.force_authenticate(user=self.normal_user)
    
    def test_user_registration(self):
        response = self.client.post(reverse('user-register-list'), {
            'username': 'newuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'newuser')