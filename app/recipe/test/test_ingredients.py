"""Test for the Ingredients API."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(email = 'test@example.com', password = 'testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientAPITests(TestCase):
    """Test the publicly available ingredients API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the ingredients API."""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientAPITests(TestCase):
    """Test the authorized user ingredients API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        "Retrieve a list of ingredients."
        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.filter(user = self.user).order_by('-name')

        serializer = IngredientSerializer(ingredients, many=True )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient is successful."""
        payload = {'name': 'Cumin'}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ingredient = Ingredient.objects.get(id=res.data['id'])
        self.assertEqual(ingredient.name, payload['name'])
        self.assertEqual(ingredient.user, self.user)

    def test_create_ingredient_invalid(self):
        """Test creating an ingredient with invalid payload fails."""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



