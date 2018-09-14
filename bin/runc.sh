#!/bin/sh
set -ex
cd /home/data/www/leobbs
pwd
ls -al
docker-compose pull
docker-compose build
docker-compose up -d