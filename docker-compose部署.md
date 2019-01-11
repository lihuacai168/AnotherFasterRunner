# FasterRunner docker-compose部署

## 一.安装docker-compose  
具体步骤请自行百度  

--------

## 二.配置docker-compose.yml和setting.py  
2.1 保存如下配置到docker-compose.yml，放入FasterRunner根目录，MYSQL_ROOT_PASSWORD为mysql root账号密码，请自行设置
```python
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
      # 目录共享,格式 本地目录:容器目录
      volumes:
      - /var/lib/mysql:/var/lib/mysql
      # 端口映射,格式 本地端口:容器端口
      ports:
      - 3306:3306
      # 容器开机启动命令
      command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci  --socket=/var/lib/mysql/mysql.sock
  
  fastrunner:
      # 构建镜像路径
      build: .
      image: fastrunner:latest
      # 依赖
      depends_on:
      - db
      privileged: true
      # 共享当前目录到容器,每次启动容器会copy本地代码
      volumes:
      - ./:/share
      ports:
      - 8000:8000
      command: /bin/sh -c '\cp -rf /share/* /usr/src/app/ && python manage.py runserver 0.0.0.0:8000'

```
2.2 更改setting.py数据库配置

PASSWORD=MYSQL_ROOT_PASSWORD  
HOST=db (docker-compose中设置的mysql容器名)

----------
## 三.构建FasterRunner镜像
注意：要将docker-compose.yml放到FasterRunner根目录  

在FasterRunner根目录执行命令：  
```python
docker-compose build
```
-------
## 四.启动容器
在FasterRunner根目录执行命令：  
```python
docker-compose up -d
```

备注：首次启动没mysql镜像时，会先pull mysql镜像再启动

-------

## 五.应用数据库表
```python
docker exec -it fastrunner容器id /bin/sh #进入容器内部

# make migrations for fastuser、fastrunner
python manage.py makemigrations fastrunner fastuser

# migrate for database
python manage.py migrate fastrunner
python manage.py migrate fastuser
```
------

备注：  
docker-compose命令：
```python
docker-compose build     # 构建镜像
docker-compose up -d     # 启动容器
docker-compose stop      # 停止容器
docker-compose restart   # 重启容器
```