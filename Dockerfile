FROM netroby/docker-apache-perl
COPY ./ /www/
COPY ./etc/leobbs.conf /etc/apache2/sites-enabled/localhost.conf
CMD /usr/sbin/apache2ctl -D FOREGROUND