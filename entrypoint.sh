#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py migrate

echo "from django.contrib.auth.models import User; print(\"Admin exists\") if User.objects.filter(username='$DJANGO_USER').exists() else User.objects.create_superuser('$DJANGO_USER', '$DJANGO_MAIL', '$DJANGO_PASSWORD')" | python manage.py shell

echo "${0}: creating icloud user and google maps api key."
python manage.py initial_data

echo "${0}: collecting statics."
python manage.py collectstatic --noinput

echo "${0}: starting gunicorn."

gunicorn icloud.wsgi:application \
	--name=root \
	--bind=0.0.0.0:8000 \
	--timeout=900 \
	--workers=3 \
	--threads=3 \
	--log-level=info \
	--reload

exec "$@"

