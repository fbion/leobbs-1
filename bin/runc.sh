#!/bin/sh
set -ex
cd /home/data/www/leobbs
pwd
ls -al
docker-compose down --rmi all -v
docker-compose up -d --build