FROM rikasai/ubuntu16.04_python3.6_faster_env:latest

MAINTAINER lihuacai

WORKDIR /opt/workspace/FasterRunner/

COPY ["start.sh", "manage.py", "uwsgi_docker.ini" ,"requirements.txt", "nginx.conf", "./"]


RUN  pip3 install -r ./requirements.txt -i \
    https://mirrors.aliyun.com/pypi/simple \
    --default-timeout=100 && \
    mkdir -p /opt/workspace/logs && \
    ln -s /opt/workspace/FasterRunner/nginx.conf /etc/nginx/sites-enabled/

EXPOSE 8000

CMD bash ./start.sh


