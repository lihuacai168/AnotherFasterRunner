FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

COPY nginx.conf /etc/nginx/conf.d/default.conf
#COPY dist/ /usr/share/nginx/html/
