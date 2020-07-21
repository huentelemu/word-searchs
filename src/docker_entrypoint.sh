#!/bin/sh

set -e

mkdir -p /huentelemu/media/
mkdir -p /huentelemu/static/

python manage.py collectstatic --noinput
#python manage.py makemigrations
python manage.py migrate
#python manage.py ensure_adminuser --username=admin \
#    --email=admin@example.com \
#    --password=pass

uwsgi --socket :80 --master --enable-threads --module wsgi --protocol=http
