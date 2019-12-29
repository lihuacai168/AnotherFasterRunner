FROM ubuntu:16.04

MAINTAINER yinquanwang

ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai
# Install required packages and remove the apt packages cache when done.

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get clean && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    wget \
    libpq-dev \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    libmysqlclient-dev \
    nginx \
    tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata

# update python version to 3.6
RUN	apt-get install -y \
    python-software-properties \
	software-properties-common && \
	add-apt-repository ppa:jonathonf/python-3.6 -y && \
	apt-get update && \
	apt-get install -y \
    python3.6 \
    python3.6-dev && \
	update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1 && \
	update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2 && \
	update-alternatives --config python3

WORKDIR /opt/workspace/FasterRunner/

COPY . .

RUN  pip3 install -r ./requirements.txt -i \
    https://mirrors.aliyun.com/pypi/simple \
    --default-timeout=100 && \
    mkdir -p /opt/workspace/logs && \
    ln -s /opt/workspace/FasterRunner/nginx.conf /etc/nginx/sites-enabled/



EXPOSE 8000

CMD bash ./start.sh


