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

    def test_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='testpass123'
            )
