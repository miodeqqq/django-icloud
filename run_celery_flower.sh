#!/usr/bin/env bash
sleep 15
celery -A icloud flower --basic_auth=icloud:icloud