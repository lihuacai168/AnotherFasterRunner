# FROM python:3.9-alpine as Base

# COPY requirements.txt .
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# RUN apk add --no-cache mariadb-connector-c-dev
# RUN apk update &&  \
#     apk add python3-dev mariadb-dev build-base netcat-openbsd linux-headers pcre-dev && \
#     pip install setuptools~=57.5.0 -i https://pypi.tuna.tsinghua.edu.cn/simple && \
#     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
#     apk del python3-dev mariadb-dev build-base linux-headers pcre-dev

#COPY requirements.txt .
#RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

FROM registry-vpc.cn-hangzhou.aliyuncs.com/cbk/fasterrunner:base-latest
ENV TZ=Asia/Shanghai
ENV LANG=C.UTF-8
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk --no-cache add tzdata mariadb-connector-c-dev linux-headers nginx uwsgi\
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone && rm -rf /var/cache/apk/*

# COPY --from=Base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /opt/workspace/FasterRunner/
COPY nginx.conf /etc/nginx/http.d/default.conf
COPY . /opt/workspace/FasterRunner/
RUN chmod +x /opt/workspace/FasterRunner/start.sh &&  \
    python manage.py collectstatic --settings=FasterRunner.settings.docker --no-input &&  \
    addgroup -g 1000 TestGroup && adduser testuser -D -G TestGroup -u 1000 &&  \
    chmod o+w /opt/workspace/FasterRunner/logs/*

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=FasterRunner.settings.docker
EXPOSE 8000

CMD [ "bash /opt/workspace/FasterRunner/start.sh" ]