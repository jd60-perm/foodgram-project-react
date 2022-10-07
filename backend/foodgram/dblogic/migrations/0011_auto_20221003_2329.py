# Generated by Django 3.2.3 on 2022-10-03 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dblogic', '0010_ingredient_ingredient_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(help_text='Добавленный рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='dblogic.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(help_text='Ингридиент, соотносимый с рецептом', on_delete=django.db.models.deletion.CASCADE, related_name='recipes_set', to='dblogic.ingredient', verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт, соотносимый с интридиентом', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_set', to='dblogic.recipe', verbose_name='Рецепт'),
        ),
    ]
