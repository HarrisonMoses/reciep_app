'''
Views for the recipe APIs. 
'''
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, status, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from core.models import (Recipe, Tag, Ingredient)
from recipe.serializers import( RecipeSerializer,
                                RecipeDetailSerializer,
                                TagSerializer,
                                IngredientSerializer,
                                RecipeImageSerializer
                            )



class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags', 'ingredients']

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return the appropriate serializer class based on action."""
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    @action(methods=['POST','PATCH'], detail = True, url_path ='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['POST'])
    # def retrieve(self, request, pk=None):
    #     """Retrieve a specific recipe."""
    #     recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    #     serializer = self.get_serializer(recipe)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class TagViewSet(mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag."""
        serializer.save(user=self.request.user)


class IngredientViewSet(mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Manage ingredients in the database."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the ingredients for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient."""
        serializer.save(user=self.request.user)