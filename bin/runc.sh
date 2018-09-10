#!/bin/sh
set -ex
cd /home/data/www/leobbs
pwd
ls -al
docker-compose down
docker-compose up -d --build