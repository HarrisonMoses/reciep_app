"""
Tests for models
"""
from unittest.mock import patch

from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from core import models

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
            recipe = models.Recipe.objects.create(user=user, **payload)
            self.assertEqual(recipe.title, payload['title'])
            self.assertEqual(recipe.user, user)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = get_user_model().objects.create_user(
                email='test2@example.com',
                password='testpass123')
        res = models.Tag.objects.create(
            user=user,
            name='Test Tag'
        )
        self.assertEqual(res.name, 'Test Tag')

    def test_creating_ingredient(self):
        """Test creating an ingredient is successful."""
        user = get_user_model().objects.create_user(
                email='test2@example.com',
                password='testpass123')

        res = models.Ingredient.objects.create(
            user=user,
            name='Test Ingredient'
        )
        self.assertEqual(str(res), res.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)