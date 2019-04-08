# FasterRunner

[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/HttpRunner/FasterRunner.svg?branch=master)](https://travis-ci.org/HttpRunner/FasterRunner) ![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)

> FasterRunner that depends FasterWeb

```

## Docker 部署 uwsgi+nginx模式
1. docker pull docker.io/mysql:5.7 # 拉取mysql5.7镜像
2. docker run --name mysql --net=host -d --restart always -v /var/lib/mysql:/var/lib/mysql -e  MYSQL_ROOT_PASSWORD=lcc123456 docker.io/mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci  # 运行mysql容器
3. 连接数据库, 新建一个db，例如fastrunner
4. 修改settings.py DATABASES 字典相关配置，NAME, USER, PASSWORD, HOST
5. 启动rabbitmq docker run -d --name --net=host --restart always rabbitmq -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
6. 修改settings.py BROKER_URL(配置rabbittmq的IP，username,password)
7. 切换到FasterRunner目录，Linux环境执行下 dos2unix ./start.sh # 因为windos编写的bash有编码问题
8. docker build -t fastrunner:latest .    # 构建docker镜像
9. docker run -d --name fastrunner --net=host --restart always fastrunner:latest  # 后台运行docker容器,默认后台端口5000
10. docker exec -it fastrunner /bin/sh  #进入容器内部
11. 应用数据库表
``` bash

# make migrations for fastuser、fastrunner
python3 manage.py makemigrations fastrunner fastuser

# migrate for database
python3 manage.py migrate fastrunner
python3 manage.py migrate fastuser
python3 manage.py migrate djcelery
```



