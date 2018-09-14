FROM perl:latest
COPY ./ /www/
RUN  cpanm Carton && cd /www
WORKDIR /www
RUN Carton install
CMD Carton exec ./main.pl daemon