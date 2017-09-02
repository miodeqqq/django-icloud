#!/usr/bin/env bash
rm -f /usr/src/app/*.pid
sleep 10
celery -A icloud.celery beat -l debug