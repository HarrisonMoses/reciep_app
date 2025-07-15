"""
urls for the recipe APIs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

app_name = 'recipe'

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
]