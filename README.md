# UEKPartnership 

[![pipeline status](https://gitlab.com/jankubierecki/UEKPartnership/badges/master/pipeline.svg)](https://gitlab.com/jankubierecki/UEKPartnership/commits/master)
[![coverage report](https://gitlab.com/jankubierecki/UEKPartnership/badges/master/coverage.svg)](https://gitlab.com/jankubierecki/UEKPartnership/commits/master)

### Mandatory system requirements
* Docker
* Docker compose

### Requirements
* [django 2.0.6](https://docs.djangoproject.com/en/2.0/)
* [psycopg2-binary](https://pypi.org/project/psycopg2-binary/2.7.4/)
* [django-admin-view-permission](https://github.com/ctxis/django-admin-view-permission)
* [gunicorn](https://pypi.org/project/gunicorn/)
* [django-compressor](https://django-compressor.readthedocs.io)
* [django-admin-list-filter-dropdown](https://github.com/mrts/django-admin-list-filter-dropdown)
* [django-modeladmin-reorder](https://github.com/mishbahr/django-modeladmin-reorder)
* [csscompressor](https://pypi.org/project/csscompressor/)
* [django-templated-email](https://github.com/vintasoftware/django-templated-email)


### Installing
1. ```docker volume create pgdata```
2. ```docker-compose up```
3. ```docker exec -it <container_id> /bin/bash```
4. ```python manage.py createsuperuser```
5. ```visit localhost:8000```


### Note
I've designed this application for the dean of my university. You can check it out at [https://wspolpracebiznesowe.uek.krakow.pl](https://wspolpracebiznesowe.uek.krakow.pl). It remains closed for now, and I don't expect this project to be develop in the nearliest future.
