#!/bin/sh

# start nginx service
service nginx start

# start celery worker
#celery multi start w1 -A FasterRunner -l info --logfile=./logs/worker.log
#python3 manage.py celery -A FasterRunner.mycelery worker -l info -P solo --settings=FasterRunner.settings.pro --logfile=./logs/worker.log 2>&1 &


# start celery beat
#nohup python3 manage.py celery beat -l info > ./logs/beat.log 2>&1 &
#nohup python3 manage.py FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
#nohup celery -A FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
#if [ -f celerybeat.pid ]; then rm celerybeat.pid;fi
#python3 manage.py  celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.pro --logfile=./logs/beat.log 2>&1 &

# start fastrunner
#uwsgi --ini ./uwsgi_docker.ini
#uwsgi --ini ./uwsgi_docker.ini  --logto ./logs/uwsgi.log
#gunicorn FasterRunner.wsgi_docker -b 0.0.0.0 -w 4
#python3 manage.py runserver --settings=FasterRunner.settings.docker

echo "--------------start app-----------------"
# /usr/local/bin/python -m gunicorn FasterRunner.wsgi_docker -b 0.0.0.0 -w 4
uwsgi --ini ./uwsgi_docker.ini  --logto ./logs/uwsgi.log

echo "--------------start celery--------------"
nohup /usr/local/bin/python manage.py celery -A FasterRunner.mycelery worker -l info --settings=FasterRunner.settings.docker --logfile=./logs/worker.log 2>&1 &

echo "--------------start celery beat---------"
nohup python manage.py celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.docker --logfile=./logs/beat.log 2>&1 &

# if [ $1 = "app" ]; then
#     echo "start app"
#     /usr/local/bin/python -m gunicorn FasterRunner.wsgi_docker -b 0.0.0.0 -w 4
# fi

# if [ $1 = "celery-worker" ]; then
#     echo "start celery"
#     /usr/local/bin/python manage.py celery -A FasterRunner.mycelery worker -l info --settings=FasterRunner.settings.docker --logfile=./logs/worker.log
# fi


# if [ $1 = "celery-beat" ]; then
#     echo "start celery beat"
#     python manage.py celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.docker --logfile=./logs/beat.log
# fi