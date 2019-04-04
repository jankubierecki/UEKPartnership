FROM python:3.6-alpine
ENV PYTHONBUFFERED 1
ENV DJANGO_SETTINGS_MODULE UEKpartnerships.production_settings


WORKDIR /partnerships
COPY requirements.txt .
EXPOSE 8000
ENTRYPOINT "/partnerships/runserver.sh"
RUN apk add netcat-openbsd postgresql-libs postgresql-dev gcc musl-dev libffi libffi-dev openssl-dev openssl py-pynacl build-base
RUN apk add libxml2-dev libxml2 libxslt libxslt-dev
RUN pip install -r requirements.txt

COPY . .

