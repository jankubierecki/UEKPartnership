#!/usr/bin/env bash
coverage run --source="." ./manage.py test --no-input
coverage report --omit="UEKpartnerships/*","manage.py","wait_for_container.py","venv/*"  --skip-covered --fail-under=50
