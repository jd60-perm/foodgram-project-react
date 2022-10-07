# Generated by Django 3.2.3 on 2022-10-07 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dblogic', '0015_alter_ingredientinrecipe_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(help_text='Ингридиент, соотносимый с рецептом', on_delete=django.db.models.deletion.CASCADE, related_name='recipes_set', to='dblogic.ingredient', verbose_name='Ингридиент'),
        ),
    ]