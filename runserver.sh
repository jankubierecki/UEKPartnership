#!/usr/bin/env bash
pip3 install -r requirements.txt
python3 manage.py collectstatic --no imput
python3 manage.py migrate
gunicorn UEKpartnerships:wsgi -b 0.0.0.0:8000
