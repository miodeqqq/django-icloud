FROM python:3.7.4-alpine3.9

MAINTAINER Maciej Januszewski<maciek@mjanuszewski.pl>

ENV PYTHONUNBUFFERED 1

ENV PG_VERSION 11.6-r0

COPY requirements.txt /tmp/

RUN set -ex \
		&& apk add --no-cache \
			 gcc \
			 g++ \
			 postgresql-dev=$PG_VERSION \
			 libjpeg-turbo-dev \
			 libffi-dev \
			 musl-dev \
			 jpeg-dev \
			 zlib-dev \
			 freetype-dev \
			 lcms2-dev \
			 openjpeg-dev \
			 tiff-dev \
			 tk-dev \
			 tcl-dev \
			 harfbuzz-dev \
			 fribidi-dev \
			 linux-headers \
		&& apk add --no-cache \
			 gettext \
			 bash \
			 libmagic \
			 postgresql-client=$PG_VERSION \
		&& apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
		        openssl \
				libressl2.7-libcrypto \
		&& apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
			 gdal-dev \
		&& pip install --upgrade pip \
		&& pip install --no-cache-dir -r /tmp/requirements.txt && rm -rf /tmp/

RUN mkdir /src

WORKDIR /src

COPY . /src

EXPOSE 8000