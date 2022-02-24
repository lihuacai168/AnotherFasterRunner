FROM fasterrunner_app:latest as Base

FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=Base  /app/static  /www/FasterRunner/static