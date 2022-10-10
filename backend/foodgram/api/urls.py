from rest_framework.routers import SimpleRouter

from django.urls import include, path, re_path

from .views import TagViewSet, IngredientViewSet, RecipeViewSet, FavoriteView, FollowView, ShoppingCartView

app_name = 'api'

router = SimpleRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'recipes/(?P<recipe_id>\d+)/favorite',
#     FavoriteViewSet,
#     basename='favorite'
# )

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteView.as_view()),
    re_path(r'users/(?P<user_id>\d+)/subscribe', FollowView.as_view()),
    re_path(r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartView.as_view()),
]
