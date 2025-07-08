"""
Viess for the User API
"""
from rest_framework import generics, permissions
from serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """
    View to create a new user in the system.
    """
    serializers = UserSerializer

