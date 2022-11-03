FROM python:3.8-bullseye

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# install django
RUN mkdir /django-padel
WORKDIR /django-padel
COPY requirements_production.txt /django-padel
RUN pip install --upgrade pip && pip install -r requirements_production.txt
COPY anmeldung /django-padel/anmeldung
COPY locale /django-padel/locale
COPY padelanalytics /django-padel/padelanalytics
COPY tournaments /django-padel/tournaments
COPY nginx/start-server.sh /django-padel
RUN chown -R www-data:www-data /django-padel
EXPOSE 8030
STOPSIGNAL SIGTERM
CMD ["/bin/sh", "-c",  "/django-padel/start-server.sh"]
