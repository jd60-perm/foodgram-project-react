import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Наименование ингридиента',
        help_text='Название продукта - не более 200 символов',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения ингридиента',
        help_text='Единица измерения: г, шт и.т.д. Не более 200 символов',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                name='Ingredient_unique',
                fields=['name', 'measurement_unit']
            )
        ]

    def __str__(self):
        return f'{self.name} / {self.measurement_unit}'


def validate_hex_color(value):
    if not (
        value[0] == '#'
        and re.fullmatch(r'^[0-9A-F]+$', value[1:])
        and len(value) == 7
    ):
        raise ValidationError(f'{value} - не является кодом цвета RGB')


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Наименование тега',
        help_text='Тег для быстрого выбора необходимых рецептов',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX',
        help_text='Код цвета в формате #HHHHHH',
        validators=[validate_hex_color, ],
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг',
        help_text='^[-a-zA-Z0-9_]+$',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        help_text='Вобор из тегов',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор заполняется автоматически',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Список ингредиентов',
        help_text='Вобор из ингридиентов',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название блюда',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Картинка',
        help_text='Загрузите картинку',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание процесса приготовления',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1, message='Значение не менее 1'), ],
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return f'''{self.name}. Кол-во добавлений в
        Избранное: {self.favorites.all().count()}'''


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_set',
        verbose_name='Рецепт',
        help_text='Рецепт, соотносимый с интридиентом',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes_set',
        verbose_name='Ингридиент',
        help_text='Ингридиент, соотносимый с рецептом',
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1, message='Значение не менее 1'), ],
        verbose_name='Количество',
        help_text='Количество согласно единицам измерения',
    )

    class Meta:
        verbose_name = 'Ингридиенты в рецептах'
        verbose_name_plural = 'Ингридиенты в рецептах'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                name='IngredientInRecipe_unique',
                fields=['recipe', 'ingredient']
            )
        ]

    def __str__(self):
        return f'Ингридиент {self.ingredient} в рецепте {self.recipe}'


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор подписки',
        help_text='Пользователь, на которого подписываются',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                name='Follow_unique',
                fields=['follower', 'following']
            )
        ]

    def __str__(self):
        return f'Подписка {self.follower} на {self.following}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Пользователь, который добавил в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Добавленный рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                name='Favorite_unique',
                fields=['user', 'recipe']
            )
        ]

    def __str__(self):
        return f'Добавление рецпта {self.recipe} в избранное {self.user}'


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь',
        help_text='Пользователь, который добавил в список покупок',
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shoppingcart',
        verbose_name='Добавленные рецепты',
        help_text='Набор рецептов для списка покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('-id',)

    def __str__(self):
        return f'Список покупок пользователя {self.user}'
