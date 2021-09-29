FROM python:3.8.11-alpine3.13
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev curl libressl-dev libxslt-dev netcat-openbsd gcc musl-dev postgresql-dev

ADD requirements.txt /.
RUN pip install -r /requirements.txt

ADD entrypoint.sh /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/entrypoint.sh"]

ADD . /code/

WORKDIR /code

# COPY .env.dev .env

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

