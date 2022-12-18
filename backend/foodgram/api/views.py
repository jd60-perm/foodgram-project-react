import io

from dblogic.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                            Tag)
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from foodgram.settings import BASE_DIR
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import User

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = AllowAny,


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = AllowAny,

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name_filter = self.request.query_params.get('name', None)
        return queryset.filter(name__istartswith=name_filter)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = IsAuthenticatedOrReadOnly,

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_in_cart_filter = self.request.query_params.get(
            'is_in_shopping_cart',
            None
        )
        if is_in_cart_filter == '1':
            try:
                cart = get_object_or_404(ShoppingCart, user=self.request.user)
            except Exception:
                queryset = Recipe.objects.none()
                return queryset
            queryset = queryset.filter(shoppingcart=cart.id)
            return queryset
        is_favorited_filter = self.request.query_params.get(
            'is_favorited',
            None
        )
        author_filter = self.request.query_params.get('author', None)
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if author_filter:
            queryset = queryset.filter(author__id=author_filter)
        if is_favorited_filter == '1':
            queryset = queryset.filter(favorites__user=self.request.user)
        return queryset

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        cart = ShoppingCart.objects.get_or_create(user=self.request.user)
        recipes = cart[0].recipe.all()
        cart_ingredients = {}
        for recipe in recipes:
            ingredients_in_recipe = recipe.ingredients_set.all()
            for ingredient_in_recipe in ingredients_in_recipe:
                name = str(ingredient_in_recipe.ingredient)
                amount = ingredient_in_recipe.amount
                if name in cart_ingredients.keys():
                    cart_ingredients[name] = cart_ingredients[name] + amount
                else:
                    cart_ingredients[name] = amount
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(
            TTFont('arial', f'{BASE_DIR}/djangostatic/arial.ttf')
        )
        p.setFont('arial', 16)
        p.drawString(100, 750, "Список покупок из проекта FOODGRAM:")
        p.setFont('arial', 12)
        textobject = p.beginText(100, 720)
        for key in cart_ingredients:
            textobject.textLine(f'- {key} - {cart_ingredients[key]}')
        p.drawText(textobject)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.pdf'
        )


class FollowView(views.APIView):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, id=self.kwargs.get('user_id'))
        obj = Follow.objects.create(follower=follower, following=following)
        serializer = FollowSerializer(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, )

    def delete(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, id=self.kwargs.get('user_id'))
        obj = get_object_or_404(Follow, follower=follower, following=following)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TemplateView(views.APIView):
    modelclass = None

    def post(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        if self.modelclass == Favorite:
            self.modelclass.objects.create(user=user, recipe=recipe)
        elif self.modelclass == ShoppingCart:
            obj = self.modelclass.objects.get_or_create(user=user)
            recipe.shoppingcart.add(obj[0].id)
        else:
            return Response('Wrong data', status=status.HTTP_400_BAD_REQUEST, )
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, )

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        if self.modelclass == Favorite:
            obj = get_object_or_404(self.modelclass, user=user, recipe=recipe)
            obj.delete()
        elif self.modelclass == ShoppingCart:
            obj = get_object_or_404(self.modelclass, user=user, recipe=recipe)
            recipe.shoppingcart.remove(obj.id)
        else:
            return Response('Wrong data', status=status.HTTP_400_BAD_REQUEST, )
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteView(TemplateView):
    modelclass = Favorite


class ShoppingCartView(TemplateView):
    modelclass = ShoppingCart
