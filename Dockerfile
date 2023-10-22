FROM python:3.9-buster as Base



COPY requirements.txt .

ARG DEBIAN_REPO="deb.debian.org"
ARG PIP_INDEX_URL="https://pypi.org/simple"

RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev python3-dev build-essential netcat-openbsd libpcre3-dev libldap2-dev libsasl2-dev && \
    pip install setuptools==57.5.0 -i ${PIP_INDEX_URL} && \
    pip install -r requirements.txt -i ${PIP_INDEX_URL} && \
    apt-get remove -y python3-dev build-essential libpcre3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.9-buster
ENV TZ=Asia/Shanghai

ARG DEBIAN_REPO="deb.debian.org"
RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list


RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

COPY --from=Base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
COPY . /app
RUN chmod +x /app/start.sh

RUN python manage.py collectstatic --settings=FasterRunner.settings.docker --no-input

ENTRYPOINT ["/app/start.sh"]

