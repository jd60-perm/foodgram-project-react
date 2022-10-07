# Generated by Django 3.2.3 on 2022-10-03 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dblogic', '0009_auto_20221003_2324'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='Ingredient_unique'),
        ),
    ]
