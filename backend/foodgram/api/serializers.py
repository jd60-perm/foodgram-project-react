from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
import base64
import datetime

from users.serializers import CustomUserSerializer
from dblogic.models import Tag, Ingredient, Recipe, ShoppingCart, Favorite, Follow, IngredientInRecipe
from django.core.files.base import ContentFile

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient')
    name = serializers.SlugRelatedField(read_only=True, source='ingredient', slug_field='name')
    measurement_unit = serializers.SlugRelatedField(read_only=True, source='ingredient', slug_field='measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name=f'IMG_{datetime.datetime.now()}.' + ext)
        return super().to_internal_value(data)


class CustomTagSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        tags = TagSerializer(value)
        return tags.data


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True,  default=serializers.CurrentUserDefault())
    tags = CustomTagSerializer(queryset=Tag.objects.all(), many=True)
    ingredients = IngredientInRecipeReadSerializer(source='ingredients_set', many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 
             'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        if not isinstance(self.context['request'].user, AnonymousUser):
            return Favorite.objects.filter(user=self.context['request'].user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if not isinstance(self.context['request'].user, AnonymousUser):
            return ShoppingCart.objects.filter(user=self.context['request'].user, recipe=obj).exists()
        return False

    def create(self, validated_data):
        if 'ingredients_set' in validated_data:
            ingredients = validated_data.pop('ingredients_set')
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author_id=self.context['request'].user.id)
        if 'tags' in locals():
            recipe.tags.set(tags)
        if 'ingredients' in locals():
            for object in ingredients:
                ingredient=object['ingredient']
                amount=object['amount']
                IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
        return recipe 

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        if 'ingredients_set' in validated_data:
            ingredients = validated_data.pop('ingredients_set')
            instance.ingredients_set.all().delete()
            for object in ingredients:
                ingredient=object['ingredient']
                amount=object['amount']
                IngredientInRecipe.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=amount
                )
        instance.save()
        return instance 