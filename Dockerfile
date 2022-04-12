# pull official base image
FROM python:3.9.4-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
<<<<<<< HEAD:src/Dockerfile
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev bash \
=======
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash \
>>>>>>> 14af9c8bc2ca074fa10474a5a6d92d05a717dae0:Dockerfile
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r /usr/src/app/requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

RUN chmod +x entrypoint.sh