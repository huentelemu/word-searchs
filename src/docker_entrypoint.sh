#!/bin/sh

set -e

mkdir -p /huentelemu/media/
mkdir -p /huentelemu/static/

python manage.py collectstatic --noinput --settings=conf.k8s
python manage.py migrate --settings=conf.k8s

#python manage.py makemigrations
#python manage.py ensure_adminuser --username=admin \
#    --email=admin@example.com \
#    --password=pass

export DJANGO_SETTINGS_MODULE=conf.k8s

uwsgi --socket :80 --master --enable-threads --module wsgi --protocol=http --settings=conf.k8s
#gunicorn wsgi:application --name django --bind 0.0.0.0:80 --workers 1 --log-level=info --preload
