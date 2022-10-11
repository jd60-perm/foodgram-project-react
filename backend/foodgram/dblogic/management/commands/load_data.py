from csv import DictReader

from dblogic.models import Ingredient
from django.core.management import BaseCommand

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from .csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Ingredient.objects.exists():
            print('data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Loading data")

        for row in DictReader(
            open('../../data/ingredients.csv', encoding='utf-8')
        ):
            ingridient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )  
            ingridient.save()
