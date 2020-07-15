#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py ensure_adminuser --username=admin \
    --email=admin@example.com \
    --password=pass

uwsgi --socket :8000 --master --enable-threads --module mysite.wsgi
