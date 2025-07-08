"""
Tests for the admin panel.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client as client
class UserAdminTests(TestCase):
    """Tests for the custom UserAdmin."""

    def setUp(self):
        """Set up a user and a superuser."""
        self.client = client()
        self.admin_user = get_user_model().objects.create_superuser(
            email ='admin@example.com',
            password='testpass123',
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email ="test@example.com",
            password="testpass123",
            name="Test User"
        )

    def test_user_listed(self):
        """Test that users are listed on the user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
