#!/bin/sh
set -ex
rsync -avzP -e " ssh" ./* root@fs.isrv.us:/home/data/www/leobbs
ssh -v root@fs.isrv.us sh /home/data/www/leobbs/bin/runc.sh