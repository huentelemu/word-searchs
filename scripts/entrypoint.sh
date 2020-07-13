#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

uwsgi --socket :8000 --master --enable-threads --module mysite.wsgi
