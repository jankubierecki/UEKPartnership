#!/usr/bin/env bash
cd /root/UEKPartnership

pip3 install -r requirements.txt

echo "Waiting for postgres"
while ! nc -z localhost 5432
do
	echo "Retrying..."
	sleep 2
done

python3 manage.py collectstatic --no-input
python3 manage.py migrate
pkill gunicorn
gunicorn UEKpartnerships.wsgi --log-file /var/log/gunicorn/error_log --access-logformat /var/log/gunicorn/access_log --daemon -b 0.0.0.0:8000
