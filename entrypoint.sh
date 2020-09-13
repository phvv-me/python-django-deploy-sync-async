#!/bin/sh

set -e

unzip my_django_project.zip

pip install -r requirements.txt

uwsgi \
     --master --enable-threads \
     --http-socket :8000 \
     --module my_django_project.my_django_project.wsgi