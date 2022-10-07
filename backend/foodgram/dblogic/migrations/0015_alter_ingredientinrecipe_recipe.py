# Generated by Django 3.2.3 on 2022-10-07 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dblogic', '0014_auto_20221007_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт, соотносимый с интридиентом', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_set', to='dblogic.recipe', verbose_name='Рецепт'),
        ),
    ]