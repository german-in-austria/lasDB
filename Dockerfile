# lasDB
FROM ubuntu:18.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# INSTALL EVERYTHING
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl gnupg \
    git \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-tk \
    nginx \
    supervisor \
    sqlite3 \
    postgresql-client \
    libtiff5-dev \
    libjpeg8-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libpq-dev \
    tcl8.6-dev \
    tk8.6-dev \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# INSTALL UWSGI
RUN pip3 install uwsgi
COPY uwsgi_params /home/docker/code/
COPY uwsgi.ini /home/docker/code/

# NGINX STANDARD SETUP
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# INSTALL PYTHON MODULES
COPY app/requirements.txt /home/docker/code/app/
RUN pip3 install -r /home/docker/code/app/requirements.txt
RUN pip3 install psycopg2

# ADD WEBPACK lasDB CODE
COPY webpack_src/lasDB /home/docker/code/webpack_src/lasDB/
RUN cd /home/docker/code/webpack_src/lasDB && npm install && npm run build

# ADD APP CODE
COPY app/ /home/docker/code/app/

RUN date '+%Y-%m-%d %H:%M:%S' > /home/docker/code/build_datetime.txt

# COLLECT ALL STATIC FILES IN /STATIC
ENV LASDB_STATIC_ROOT=/static
RUN python3 /home/docker/code/app/manage.py collectstatic --noinput

EXPOSE 80
CMD ["supervisord", "-n"]
