#!/bin/sh
echo "--------------start nginx--------------"
nginx

echo "--------------start app--------------"
uwsgi --ini ./ComposeDeploy/uwsgi_docker.ini
# uwsgi --ini ./ComposeDeploy/uwsgi_docker.ini --logto ./logs/uwsgi.log
# /usr/local/bin/python manage.py runserver 0.0.0.0:8000 --settings=FasterRunner.settings.docker

echo "--------------start celery worker--------------"
export DJANGO_SETTINGS_MODULE=FasterRunner.settings.docker;
nohup python -m celery -A FasterRunner.mycelery worker -l info --uid=1000 > ./logs/worker.log 2>&1 &
# nohup /usr/local/bin/python manage.py celery -A FasterRunner.mycelery worker -l info --settings=FasterRunner.settings.docker --logfile=./logs/worker.log 2>&1 &
#celery multi start w1 -A FasterRunner -l info --logfile=./logs/worker.log
#python3 manage.py celery -A FasterRunner.mycelery worker -l info -P solo --settings=FasterRunner.settings.pro --logfile=./logs/worker.log 2>&1 &

echo "--------------start celery beat--------------"
# nohup python manage.py celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.docker --logfile=./logs/beat.log 2>&1 &
export DJANGO_SETTINGS_MODULE=FasterRunner.settings.docker;
nohup python -m celery -A FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
#nohup python3 manage.py celery beat -l info > ./logs/beat.log 2>&1 &
#nohup python3 manage.py FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
#nohup celery -A FasterRunner.mycelery beat -l info > ./logs/beat.log 2>&1 &
#if [ -f celerybeat.pid ]; then rm celerybeat.pid;fi
#python3 manage.py  celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.pro --logfile=./logs/beat.log 2>&1 &


# if [ $1 = "app" ]; then
#     echo "start app"
#     /usr/local/bin/python -m gunicorn FasterRunner.wsgi_docker -b 0.0.0.0 -w 4
# fi

# if [ $1 = "celery-worker" ]; then
#     echo "start celery"
#     export DJANGO_SETTINGS_MODULE=FasterRunner.settings.docker; /usr/local/bin/python -m celery -A FasterRunner.mycelery worker -l info
# fi

# if [ $1 = "celery-beat" ]; then
#     echo "start celery beat"
#     python manage.py celery -A FasterRunner.mycelery beat -l info --settings=FasterRunner.settings.docker --logfile=./logs/beat.log
# fi

# if [ $1 = "celery-beat" ]; then
#     echo "start celery beat"
#     export DJANGO_SETTINGS_MODULE=FasterRunner.settings.docker; /usr/local/bin/python -m celery -A FasterRunner.mycelery beat -l info
# fi