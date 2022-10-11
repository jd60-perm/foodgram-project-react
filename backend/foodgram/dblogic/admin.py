from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    fields = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    fields = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.display(description='Кол-во добавлений в Избранное')
def favorites_quantity(obj):
    return (obj.favorites.all().count())


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', favorites_quantity)
    fields = ('name', 'author', 'text', 'cooking_time', 'tags', 'image')
    search_fields = ('name',)
    list_filter = ('tags', 'author')
    filter_horizontal = ('tags',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    fields = ('recipe', 'ingredient', 'amount')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    fields = ('follower', 'following')
    list_filter = ('follower', 'following')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe')
    list_filter = ('user',)
