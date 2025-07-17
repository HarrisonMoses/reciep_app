'''
serilizers for the recipe APIs.
'''
from rest_framework import serializers
from core.models import (Recipe, Tag , Ingredient)

class TagSerializer(serializers.ModelSerializer):
    '''Serializer for the tag object.'''
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for the recipe object.'''
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ('id',)

    def _get_or_create_tags(self, tags:list, recipe):
        '''Handle getting or creating tags for recipe.'''
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        '''Create a recipe with tags.'''
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        '''Update a recipe with tags.'''
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']




class IngredientSerializer(serializers.ModelSerializer):
    '''Serializer for the ingredient object.'''
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)

