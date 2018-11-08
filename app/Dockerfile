# docker build -t ec2-deploy:base -f Dockerfile.base .
FROM        python:3.6.7-slim
MAINTAINER  folivoradev@gmail.com
ENV         LANG                    C.UTF-8

RUN         apt -y update
RUN         apt -y dist-upgrade
RUN         apt -y install gcc nginx supervisor && \
            pip3 install uwsgi && \
            apt -y remove gcc && \
            apt -y autoremove

COPY        requirements-production.txt /tmp/requirements.txt
RUN         pip3 install -r /tmp/requirements.txt
# docker build -t eb:docker -f Dockerfile .
FROM        folivoradev/eb-docker:base
ENV         DJANGO_SETTINGS_MODULE  config.settings.production

# 전체 소스코드 복사
COPY        ./   /srv/project
WORKDIR     /srv/project

# 프로세스를 실행할 명령
WORKDIR     /srv/project/app
RUN         python3 manage.py collectstatic --noinput

# Nginx
RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

# supervisor설정파일 복사
RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

# 80번 포트 개방
EXPOSE      80

# Command로 supervisor실행
CMD         supervisord -n