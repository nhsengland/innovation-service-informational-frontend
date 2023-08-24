#!/bin/sh

apt-get update
apt-get -y install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev

# Cherry pick update folders for performance reasons when deploying
# More information here: https://docs.wagtail.org/en/stable/releases/3.0.html#upgrade-considerations-changes-affecting-all-projects
echo "Applying custom commands"
wagtail updatemodulepaths antenv/lib/python3.10/site-packages/wagtail/snippets/tests
wagtail updatemodulepaths antenv/lib/python3.10/site-packages/wagtail/tests
wagtail updatemodulepaths antenv/lib/python3.10/site-packages/wagtail_pdf_view
wagtail updatemodulepaths antenv/lib/python3.10/site-packages/wagtailnhsukfrontend
echo "Finished applying custom commands"

python3 manage.py collectstatic --clear --noinput
python3 manage.py compress

#gunicorn --bind=0.0.0.0 --timeout 600 is_homepage.wsgi
python3 -u manage.py runserver 0.0.0.0:8000
