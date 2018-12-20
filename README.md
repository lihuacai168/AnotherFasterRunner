# FasterRunner

[![LICENSE](https://img.shields.io/github/license/yinquanwang/FasterRunner.svg)](https://github.com/yinquanwang/FasterRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/yinquanwang/FasterRunner.svg?branch=master)](https://travis-ci.org/yinquanwang/FasterRunner) ![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)

> FasterRunner that depends FasterWeb


## Build Development

``` bash
# install requirements.txt
pip install -r requirements.txt

# make migrations for fastuser、fastrunner
python manage.py makemigrations fastrunner fastuser

# migrate for database
python manage.py migrate

# runserver in dev
python manage.py runserver

```

## Docker 部署
1. docker pull docker.io/mysql:5.7 # 拉取mysql5.7镜像
2. docker run --name mysql --net=host -d --restart always -v /var/lib/mysql:/var/lib/mysql -e  MYSQL_ROOT_PASSWORD=lcc123456 docker.io/mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci  # 运行mysql容器
3. 修改settings.py DATABASES 字典相关配置，密码为步骤2设置的MYSQL_ROOT_PASSWORD
4. 连接数据库, 新建FasterRunner库
5. docker build -t FasterRunner:latest .    # 构建docker镜像
6. docker run -d --name fastrunner --net=host --restart always FasterRunner:latest  # 后台运行docker容器
7. docker exec -it fastrunner /bin/sh  #进入容器内部
8. 应用数据库表
``` bash

# make migrations for fastuser、fastrunner
python manage.py makemigrations fastrunner fastuser

# migrate for database
python manage.py migrate

```




