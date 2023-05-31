<h1 align="center"> Foodgram </h1>

<p align="center">
  <a href="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
    <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
  </a>
  <a href="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
    <img alt="DjangoREST" src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
  </a>
  <a href="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB">
    <img alt="Postgres" src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB">
  </a>
  <a href="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
  </a>
  <a href="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
  </a>

Проект продуктового помощника. С его помощью можно легко подготовить список покупок для выбранных рецептов.
Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.
</p>

## Установка

Как развернуть проект на локальной машине.

1. Создайте `.env` файл в каталоге `infra/` с переменными окружения:

```
DB_HOST=localhost
DB_PORT=5432
DB_ENGINE=django.db.backends.postgresql
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_DB=postgres
DEBUG=True
```

2. Убедитесь, что установили `docker` и перейдите в каталог с инфраструктурой проекта. Запустите контейнер базы данных

```
docker compose up -d db
```

3. Убедитесь, что установили `NodeJS` и перейдите в каталог с фронтендом. Установив зависимости, запустите фронтенд:

```
cd frontend/
npm i
npm run start
```

4. Перейдите в каталог с бекендом. Создайте и активируйте окружение и установите зависимости:

```
cd backend/
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

5. Выполните миграции

```
cd foodgram
python3 manage.py makemigrations
python3 manage.py migrate
```

6. Заполните таблицу ингредиентов в базе данных

```
python manage.py import_ingredients ../../data/ingredients.csv
```

7. Запуск сервера

```
python3 manage.py runserver
```

## Author

**Copyright © 2023, [Alexey Alexandrov](https://github.com/aaaaaaaalesha)**