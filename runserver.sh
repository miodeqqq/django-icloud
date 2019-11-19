#!/bin/sh

clear; docker build . -t icloud && docker-compose -f docker-compose.yml -p 'django_icloud' up --remove-orphans