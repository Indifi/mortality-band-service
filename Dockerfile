FROM 583289034972.dkr.ecr.ap-south-1.amazonaws.com/analytics-engine-base:v6

# Copy requirements file
COPY requirements.txt /requirements.txt

RUN pip3.6 install --no-cache-dir -r /requirements.txt \
    && mkdir /code/

WORKDIR /code/
COPY . /code/

#RUN cp deployment_config/uwsgi.service /etc/systemd/system

# Add any custom, static environment variables needed by Django or settings file:
ENV DJANGO_SETTINGS_MODULE="config.settings.prod" PYTHONUNBUFFERED=1
ENV COMMAND="abc" DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

# uWSGI will listen on this port
EXPOSE 80

RUN rm /etc/nginx/sites-available/default \
    && cp deployment_config/default /etc/nginx/sites-available/ \
    && mkdir /etc/uwsgi \
    && mkdir /etc/uwsgi/sites \
    && cp deployment_config/analytics_furnace.ini /etc/uwsgi/sites/ \
    && mkdir /var/log/uwsgi \
    && /bin/bash -c "source ~/.bash_aliases" \
    && ln -s /usr/local/lib/python3.6 python

CMD ${COMMAND}