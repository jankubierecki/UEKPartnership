#!/usr/bin/env bash

echo "Waiting for postgres"
while ! nc -z postgres 5432
do
	echo "Retrying..."
	sleep 2
done

python manage.py collectstatic --no-input
python manage.py migrate

gunicorn UEKpartnerships.wsgi --log-file /var/log/gunicorn/log --access-logformat /var/log/gunicorn/access_log --workers=${NUMBER_OF_CORES} -b 0.0.0.0:8000

