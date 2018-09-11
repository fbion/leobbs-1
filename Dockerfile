FROM perl:latest
COPY ./ /www/
RUN  cpanm Mojolicious && cd /www
WORKDIR /www
CMD perl ./main.pl daemon