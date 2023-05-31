import os
import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Ingredient'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Путь к CSV файлу')

    def handle(self, path: str, *args, **options):
        print('Заполнение модели Ingredient из CSV запущено')
        if not (os.path.exists(path) and path.endswith('.csv')):
            print(f'Файла {path} не существует или не поддерживает формат CSV')
            return

        with open(path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    if not created:
                        print(
                            f'Ингредиент {obj} уже существует'
                        )
                except Exception as error:
                    print(f'Ошибка в строке {row}: {error}')

        print('Заполнение модели Ingredient успешно завершено')
