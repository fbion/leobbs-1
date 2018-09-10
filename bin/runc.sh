#!/bin/sh
set -ex
cd /home/data/www/leobbs
pwd
ls -al
docker-compose pull
docker-compose down --rmi all -v
docker-compose build --no-cache  --force-rm
docker-compose up -d