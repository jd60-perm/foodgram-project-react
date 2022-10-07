# Generated by Django 3.2.3 on 2022-10-02 21:24

import dblogic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Название продукта - не более 200 символов', max_length=200, unique=True, verbose_name='Наименование ингридиента')),
                ('measurement_unit', models.CharField(help_text='Единица измерения: г, кг, шт, л, мл и.т.д. Не более 200 символов', max_length=200, verbose_name='Единица измерения ингридиента')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Тег для быстрого выбора необходимых рецептов', max_length=200, unique=True, verbose_name='Наименование тега')),
                ('color', models.CharField(help_text='Код цвета в формате #HHHHHH', max_length=7, unique=True, validators=[dblogic.models.validate_hex_color], verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(help_text='^[-a-zA-Z0-9_]+$', max_length=200, unique=True, verbose_name='Уникальный слаг')),
            ],
        ),
    ]