FROM python:3.6
ENV PYTHONBUFFERED 1
ENV DJANGO_SETTINGS_MODULE UEKpartnerships.production_settings

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /partnerships
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
ENTRYPOINT "/partnerships/runserver.sh"

