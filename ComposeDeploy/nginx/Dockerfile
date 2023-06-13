FROM fasterrunner_app:latest as Base

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=Base  /app/static_root  /www/FasterRunner/static