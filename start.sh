#!/usr/bin/env bash

# start nginx service
service nginx start

# start celery worker
#celery multi start w1 -A FasterRunner -l info --logfile=./logs/worker.log
celery multi start w1 -A FasterRunner.mycelery -l info --logfile=./logs/worker.log

# start celery beat
#nohup python3 manage.py celery beat -l info > ./logs/beat.log 2>&1 &
#nohup python3 manage.py FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
nohup celery -A FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &

# start fastrunner
uwsgi --ini ./uwsgi_docker.ini
