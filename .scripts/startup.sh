#!/bin/sh

apt-get update
apt-get -y install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev

#gunicorn --bind=0.0.0.0 --timeout 600 is_homepage.wsgi
python3 -u manage.py runserver 0.0.0.0:8000
