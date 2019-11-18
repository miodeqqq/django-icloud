#!/bin/bash

sleep 10
celery -A icloud worker -l info -Q update_icloud_data -n update_icloud_data@%h -Ofair --autoscale=10,10 --maxtasksperchild=10