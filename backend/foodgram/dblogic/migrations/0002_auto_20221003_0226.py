# Generated by Django 3.2.3 on 2022-10-02 21:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dblogic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Количество согласно единицам измерения', validators=[django.core.validators.MinValueValidator(1, message='Введите значение не менее 1')], verbose_name='Количество')),
                ('ingridient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_set', to='dblogic.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название блюда', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Загрузите картинку', upload_to='static/images/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Описание процесса приготовления', verbose_name='Описание')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Введите значение не менее 1')], verbose_name='Время приготовления (в минутах)')),
                ('author', models.ForeignKey(help_text='Автор заполняется автоматически', on_delete=django.db.models.deletion.CASCADE, related_name='resipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('ingridients', models.ManyToManyField(help_text='Вобор из ингридиентов', through='dblogic.IngredientInRecipe', to='dblogic.Ingredient', verbose_name='Список ингредиентов')),
                ('tags', models.ManyToManyField(help_text='Вобор из тегов', to='dblogic.Tag', verbose_name='Список тегов')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingridients_set', to='dblogic.recipe'),
        ),
    ]