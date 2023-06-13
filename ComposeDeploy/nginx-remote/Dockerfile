FROM rikasai/fast-runner-backend:latest as Base

FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=Base  /app/static_root  /www/FasterRunner/static