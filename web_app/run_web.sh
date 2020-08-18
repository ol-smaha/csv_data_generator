#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

rm /code/celery*.pid

celery multi start 1 -A config -l info --logfile=/code/logs/%n%I.log

gunicorn --access-logfile - --workers 4 --timeout 300 --reload \
  --bind web:8000 config.wsgi:application
