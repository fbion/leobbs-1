FROM netroby/docker-apache-perl
COPY ./* /var/www/html/
COPY ./etc/leobbs.conf /etc/apache2/sites-enabled/localhost.conf
CMD /usr/sbin/apache2ctl -D FOREGROUND