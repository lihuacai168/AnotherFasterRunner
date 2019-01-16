# FasterRunner

[![LICENSE](https://img.shields.io/github/license/yinquanwang/FasterRunner.svg)](https://github.com/yinquanwang/FasterRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/yinquanwang/FasterRunner.svg?branch=master)](https://travis-ci.org/yinquanwang/FasterRunner) ![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)

> FasterRunner that depends FasterWeb


## 本地开发环境部署

``` bash
# install requirements.txt
pip install -r requirements.txt

# make migrations for fastuser、fastrunner、fasttask
python manage.py makemigrations fastrunner fastuser fasttask

# migrate for database
python manage.py migrate fastrunner
python manage.py migrate fastuser
python manage.py migrate fasttask

# runserver in dev
python manage.py runserver

```

## Docker 部署 uwsgi+nginx模式
1. docker pull docker.io/mysql:5.7 # 拉取mysql5.7镜像
2. docker run --name mysql --net=host -d --restart always -v /var/lib/mysql:/var/lib/mysql -e  MYSQL_ROOT_PASSWORD=lcc123456 docker.io/mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci  # 运行mysql容器
3. 修改settings.py DATABASES 字典相关配置，密码为步骤2设置的MYSQL_ROOT_PASSWORD
4. 连接数据库, 新建FasterRunner库
5. docker build -t fastrunner:latest .    # 构建docker镜像
6. docker run -d --name fastrunner --net=host --restart always fastrunner:latest  # 后台运行docker容器,默认后台端口5000
7. docker exec -it fastrunner /bin/sh  #进入容器内部
8. 应用数据库表
``` bash

# make migrations for fastuser、fastrunner、fasttask
python manage.py makemigrations fastrunner fastuser

# migrate for database
python manage.py migrate fastrunner
python manage.py migrate fastuser
python manage.py migrate fasttask

```

## 在线体验地址-可能不会和GIT最新代码同步哦，建议自己docker部署
-------------
[FasterRunner 接口自动化测试平台](http://39.108.239.78:8082/#/fastrunner/register)




