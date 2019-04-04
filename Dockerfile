FROM python:3.6-alpine
ENV PYTHONBUFFERED 1
ENV DJANGO_SETTINGS_MODULE UEKpartnerships.production_settings

WORKDIR /partnerships
COPY requirements.txt .
EXPOSE 8000
ENTRYPOINT "/partnerships/runserver.sh"
RUN apk add --no-cache --virtual .build-deps netcat-openbsd postgresql-libs postgresql-dev gcc musl-dev libffi libffi-dev openssl-dev openssl py-pynacl build-base \
libxml2-dev libxml2 libxslt libxslt-dev \
&& pip install -r requirements.txt && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps
COPY . .

