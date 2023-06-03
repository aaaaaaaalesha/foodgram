FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY foodgram/ .

RUN python3 manage.py migrate --noinput
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py import_ingredients data/ingredients.csv

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
