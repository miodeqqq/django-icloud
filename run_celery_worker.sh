#!/bin/bash

celery -A icloud.celery worker -l info -Q update_icloud_data -n update_icloud_data@%h -Ofair