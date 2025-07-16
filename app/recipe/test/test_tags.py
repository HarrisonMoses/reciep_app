'''
Tests for the tags APIs.
'''
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

CREATE_TAG_URL = reverse('recipe:tag-list')

def create_user(email = 'test@example.com', password = 'testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password )


class PublicTagAPITests(TestCase):
    """Test the publicly available tags API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the tags API."""
        res = self.client.get(CREATE_TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagAPITests(TestCase):
    """Test the authorized user tags API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_create_tag_successful(self):
        """Test creating a new tag is successful."""
        payload = {'name': 'Vegan'}

        res = self.client.post(CREATE_TAG_URL, payload)
        tag = Tag.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tag.name, payload['name'])
        self.assertEqual(tag.user, self.user)

    def test_create_tag_invalid(self):
        """Test creating a tag with invalid payload fails."""
        payload = {'name': ''}

        res = self.client.post(CREATE_TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags(self):
        """Test retrieving tags for authenticated user."""
        Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')

        res = self.client.get(CREATE_TAG_URL)
        tags = Tag.objects.filter(user=self.user).order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
