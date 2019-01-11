version: '3'
services:
  # 容器名
  db: 
      # 镜像
      image: docker.io/mysql:5.7
      # 获取root权限
      privileged: true
      # 环境变量
      environment:
      - MYSQL_DATABASE=FasterRunner
      - MYSQL_ROOT_PASSWORD=123456
      # 目录共享,格式 宿主机目录:容器目录
      volumes:
      - /var/lib/mysql:/var/lib/mysql
      # 端口映射,格式 宿主机端口:容器端口
      ports:
      - 3306:3306
      # 容器开机启动命令
      command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci  --socket=/var/lib/mysql/mysql.sock
  
  fasterunner:
      build: /root/workspace/FasterRunner
      image: fasterunner:latest
      # 依赖
      depends_on:
      - db
      privileged: true
      # 共享目录到容器,每次启动容器会copy宿主机代码
      volumes:
      - /root/workspace/FasterRunner:/share/fasterunner
      ports:
      - 8000:8000
      command: /bin/sh -c '\cp -rf /share/fasterunner/* /usr/src/app/ && python manage.py runserver 0.0.0.0:8000'
   
  fasterweb:
      build: /root/workspace/FasterWeb
      image: fasterweb:latest
      # 依赖
      privileged: true
      # 共享目录到容器,每次启动容器会copy宿主机代码
      volumes:
      - /root/workspace/FasterWeb:/share/fasterweb
      ports:
      - 8082:8082
      command: /bin/sh -c '\cp -rf /share/fasterweb/default.conf /etc/nginx/conf.d/ && \cp -rf /share/fasterweb/dist/  /usr/share/nginx/html/ && nginx -g "daemon off;"'