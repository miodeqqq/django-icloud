#!/bin/bash

rm -f /code/*.pid
sleep 10
celery -A icloud.celery beat -l debug