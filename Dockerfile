FROM perl:latest
COPY ./ /www/
WORKDIR /www
CMD perl -Ilocal/lib/perl5 ./main.pl daemon