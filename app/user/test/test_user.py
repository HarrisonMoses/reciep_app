'''
Tests for the user API
'''
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Create and return a user with given parameters."""
    user =get_user_model().objects.create_user(**params)
    return user

class PublicUserAPITests(TestCase):
    """Test the publicly available user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'Test@example.com',
            'password': 'testpass',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test error returned if user already exists."""
        payload = {
            'email': ' test@example.com',
            'password': 'testpass',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test error returned if password is less than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
            """Test generates token for valid credentials."""
            payload = {
                'email': 'test@example.com',
                'password': 'testpass'
            }
            create_user(**payload)
            res = self.client.post(CREATE_TOKEN_URL, payload)
            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test returns error if credentials are invalid."""
        create_user(email='test@example.com', password='testpass')
        payload = {
            'email': 'test@example.com',
            'password': 'wrong'
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test returns error if user doesn't exist."""
        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
