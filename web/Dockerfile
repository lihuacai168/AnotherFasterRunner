FROM hub.c.163.com/library/nginx

RUN rm /etc/nginx/conf.d/default.conf

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
