"""
Tests for the recipe APIs
"""
from decimal import Decimal

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from core import models
from recipe.serializers import RecipeDetailSerializer

CREATE_RECIPE_URL = reverse('recipe:recipe-list')
def create_recipe(user, **params):
    """create and return a recipe."""
    recipe ={
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': Decimal('5.00'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe'
    }
    recipe.update(params)
    recipe['user'] = user
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test the publicly available recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_unauthorized(self):
        """Test that authentication is required to create a recipe."""
        payload = {
            'title': 'Test Recipe',
            'time_minutes': 30,
            'price': 5.99,
            'description': 'Test description',
            'link': 'http://example.com/recipe'
        }
        res = self.client.post(CREATE_RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    """Test the authorized user recipe API."""

    def setUp(self):
        self.client = APIClient()
        self.user = models.User.objects.create_user(
            email = 'test@example.com',
            password = 'testpass123',
        )
        self.client.force_authenticate(user=self.user)

    def test_create_recipe_successful(self):
        '''Create a new recipe with valid payload is successful.'''
        payload = create_recipe(user=self.user)
        res = self.client.post(CREATE_RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_recipe_successful(self):
        '''Update an existing recipe with valid payload is successful.'''
        payload = create_recipe(user=self.user)
        res = self.client.post(CREATE_RECIPE_URL, payload)
        recipe_id = res.data['id']

        update_payload = {
            'title': 'Updated Recipe',
            'time_minutes': 20,
            'price': Decimal(10.00),
            'description': 'Updated description',
            'link': 'http://example.com/updated-recipe'
        }

        update_url = reverse('recipe:recipe-detail', args=[recipe_id])
        res = self.client.put(update_url, update_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_recipe_detail(self):
        """Retrieve a specific recipe."""
        recipe = create_recipe(user=self.user)
        response = self.client.post(CREATE_RECIPE_URL, recipe)

        recipe_id = response.data['id']
        detail_url = reverse('recipe:recipe-detail', args=[recipe_id])

        res = self.client.get(detail_url)

        # Get the actual recipe object from the database
        recipe_obj = models.Recipe.objects.get(id=recipe_id)
        serializer = RecipeDetailSerializer(recipe_obj)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_recipe(self):
        """Delete a specific recipe."""
        recipe = create_recipe(user=self.user)
        response = self.client.post(CREATE_RECIPE_URL, recipe)

        recipe_id = response.data['id']
        delete_url = reverse('recipe:recipe-detail', args=[recipe_id])

        res = self.client.delete(delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the recipe is deleted
        self.assertFalse(models.Recipe.objects.filter(id=recipe_id).exists())

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags."""
        payload = {
            'title': 'Sample Recipe',
            'time_minutes': 10,
            'price': Decimal('5.00'),
            'description': 'Sample description',
            'link': 'http://example.com/recipe',
            'tags': [{'name': 'Breakfast'}, {'name': 'Vegan'}]
        }

        res = self.client.post(CREATE_RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = models.Recipe.objects.get(id=res.data['id'])
        self.assertEqual(recipe.tags.count(), 2)

        # Check that the tags were created with the correct names
        tag_names = [tag.name for tag in recipe.tags.all()]
        self.assertIn('Breakfast', tag_names)
        self.assertIn('Vegan', tag_names)

    def test_update_recipe_with_tags(self):
        """Test updating a recipe with tags."""
        payload = create_recipe(user=self.user)
        res = self.client.post(CREATE_RECIPE_URL, payload)
        recipe_id = res.data['id']

        update_payload = {
            'title': 'Updated Recipe',
            'time_minutes': 20,
            'price': Decimal(10.00),
            'description': 'Updated description',
            'link': 'http://example.com/updated-recipe',
            'tags': [{'name': 'Dinner'}, {'name': 'Healthy'}]
        }

        update_url = reverse('recipe:recipe-detail', args=[recipe_id])

        res = self.client.put(update_url, update_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe = models.Recipe.objects.get(id=recipe_id)
        self.assertEqual(recipe.tags.count(), 2)

        tag_names = [tag.name for tag in recipe.tags.all()]
        self.assertIn('Dinner', tag_names)
        self.assertIn('Healthy', tag_names)

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients."""
        payload = {
            'title': 'Sample Recipe',
            'time_minutes': 10,
            'price': Decimal('5.00'),
            'description': 'Sample description',
            'link': 'http://example.com/recipe',
            'ingredients': [{'name': 'Eggs'}, {'name': 'Milk'}]
        }

        res = self.client.post(CREATE_RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = models.Recipe.objects.get(id=res.data['id'])
        self.assertEqual(recipe.ingredients.count(), 2)

        ingredient_names = [ingredient.name for ingredient in recipe.ingredients.all()]
        self.assertIn('Eggs', ingredient_names)
        self.assertIn('Milk', ingredient_names)