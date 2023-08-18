#!/bin/sh

apt-get update
apt-get -y install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev

echo "fixing wagtail import paths"
for A in $(python -c 'import sys; [print(p) for p in sys.path if "site-packages" in p]') ; do wagtail updatemodulepaths $A ; done
echo "i've ended fixing wagtail import paths"

python3 manage.py collectstatic --clear --noinput
python3 manage.py compress

#gunicorn --bind=0.0.0.0 --timeout 600 is_homepage.wsgi
python3 -u manage.py runserver 0.0.0.0:8000
