#!/usr/bin/env bash
# start nginx service
service nginx start
# start celery worker
celery multi start w1 -A FasterRunner -l info --logfile=./logs/worker.log
# start celery beat
nohup python3 manage.py celery beat -l info > ./logs/beat.log 2>&1 &
# start fastrunner
uwsgi --ini ./uwsgi.ini