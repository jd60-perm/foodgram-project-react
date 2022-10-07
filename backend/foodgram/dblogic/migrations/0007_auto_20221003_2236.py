# Generated by Django 3.2.3 on 2022-10-03 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dblogic', '0006_auto_20221003_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientinrecipe',
            old_name='ingridient',
            new_name='ingredient',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='ingridients',
            new_name='ingredients',
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_set', to='dblogic.recipe'),
        ),
    ]
