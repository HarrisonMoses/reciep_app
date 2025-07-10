"""
Views for the User API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from serializers import UserSerializer, AuthenticationSerializer

class CreateUserView(generics.CreateAPIView):
    """
    View to create a new user in the system.
    """
    serializers = UserSerializer



    

class CreateTokenView(generics.CreateAPIView):
    serialisers = AuthenticationSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES





class UpdateUserView(generics.RetrieveUpdateAPIView):
    """View to updated the authenticated user details."""
    serializers = UserSerializer
    authentication_classes = (authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated)

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

