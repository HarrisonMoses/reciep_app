"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        User = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(User.email, email)
        self.assertTrue(User.check_password(password))

