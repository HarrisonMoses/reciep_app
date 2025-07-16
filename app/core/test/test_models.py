"""
Tests for models
"""
from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from core.models import (
    Recipe,
    Tag
)


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

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test@example.com'
        password = 'testpass123'
        User = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(User.email, email)
        self.assertTrue(User.is_staff)

    def test_create_recipe(self):
            """Test creating a recipe is successful."""
            user = get_user_model().objects.create_user(
                email='test@example.com',
                password='testpass123'
                )
            payload = {
                'title': 'Test Recipe',
                'time_minutes': 30,
                'price': Decimal('5.99'),
                'description': 'Test description',
                'link': 'http://example.com/test-recipe'
            }
            recipe = Recipe.objects.create(user=user, **payload)
            self.assertEqual(recipe.title, payload['title'])
            self.assertEqual(recipe.user, user)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = get_user_model().objects.create_user(
                email='test2@example.com',
                password='testpass123')
        res = Tag.objects.create(
            user=user,
            name='Test Tag'
        )
        self.assertEqual(res.name, 'Test Tag')