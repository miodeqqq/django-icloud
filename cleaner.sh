#!/bin/sh

clear;find . -name "*.pyc" -exec rm -f {} \; && \
rm -rf ./.cache/ && \
rm -rf logs/ && \
rm -rf media/ && \
rm -rf .DS_Store && \
rm -rf *.pid && \
rm -rf celerybeat-schedule && \
rm -rf nginx_logs && \
rm -rf static/admin/ && \
rm -rf static/cms/ && \
rm -rf static/ckeditor/ && \
rm -rf static/suit/ && \
docker rm $(docker ps -a -q) -f && \
docker volume rm `docker volume ls -q -f dangling=true` && \
echo y |docker system prune && \
echo y | docker volume prune