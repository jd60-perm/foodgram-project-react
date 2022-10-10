from django import views
from rest_framework import views
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import User
from dblogic.models import Tag, Ingredient, Recipe, Favorite, Follow, ShoppingCart
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteSerializer, FollowSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name_filter = self.request.query_params.get('name', None)
        print(name_filter)
        queryset = queryset.filter(name__istartswith=name_filter)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    search_fields = ('^name',)


    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_cart_filter = self.request.query_params.get('is_in_shopping_cart', None)
        if is_in_cart_filter == '1':
            try:
                cart = get_object_or_404(ShoppingCart, user=self.request.user)
            except Exception:
                queryset = Recipe.objects.none()
                return queryset
            queryset=queryset.filter(shoppingcart=cart.id)
            return queryset
        is_favorited_filter = self.request.query_params.get('is_favorited', None)
        author_filter = self.request.query_params.get('author', None)
        tags = self.request.query_params.getlist('tags')
        queryset=queryset.filter(tags__slug__in=tags).distinct()
        if author_filter:
            queryset=queryset.filter(author__id=author_filter)
        if is_favorited_filter == '1':
            queryset=queryset.filter(favorites__user=self.request.user)
        return queryset


class FavoriteView(views.APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        obj = Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(obj.recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, )

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        ###  Вставить обработку 400
        obj = Favorite.objects.get(user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowView(views.APIView):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = User.objects.get(id=self.kwargs.get('user_id'))
        obj = Follow.objects.create(follower=follower, following=following)
        serializer = FollowSerializer(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, )

    def delete(self, request, *args, **kwargs):
        follower = self.request.user
        following = User.objects.get(id=self.kwargs.get('user_id'))
        ###  Вставить обработку 400
        obj = Follow.objects.get(follower=follower, following=following)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(views.APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        obj = ShoppingCart.objects.get_or_create(user=user)
        recipe.shoppingcart.add(obj[0].id)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, )

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        ###  Вставить обработку 400
        obj = ShoppingCart.objects.get(user=user, recipe=recipe)
        recipe.shoppingcart.remove(obj.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
