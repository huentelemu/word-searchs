#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email admin@example.com

uwsgi --socket :8000 --master --enable-threads --module mysite.wsgi
