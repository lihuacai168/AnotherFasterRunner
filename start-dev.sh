#!/bin/sh

if [ $1 = "app" ]; then
    echo "start app"
#    /usr/local/bin/python -m gunicorn FasterRunner.wsgi_docker -b 0.0.0.0 -w4
#    export  IS_PERF=1; python -m gunicorn FasterRunner.wsgi_dev -b 0.0.0.0 -w16 -k gevent
    export IS_PERF=1; gunicorn FasterRunner.wsgi_dev -b 0.0.0.0:8000 -w 2 -k gevent
fi

if [ $1 = "worker" ]; then
    echo "start celery"
    export DJANGO_SETTINGS_MODULE=FasterRunner.settings.dev; python -m celery -A FasterRunner.mycelery worker -l error --concurrency=2
fi


if [ $1 = "beat" ]; then
    echo "start celery beat"
    export DJANGO_SETTINGS_MODULE=FasterRunner.settings.dev; python -m celery -A FasterRunner.mycelery beat -l info
fi