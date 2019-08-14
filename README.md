# FasterRunner后端部署

[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/HttpRunner/FasterRunner.svg?branch=master)](https://travis-ci.org/HttpRunner/FasterRunner) ![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)


## Docker部署 
### 1.拉取和运行MySQL
- 拉取docker mysql镜像 `docker pull docker.io/mysql:5.7 `
- 运行docker mysql容器
`docker run --name mysql --net=host -d --restart always -v /var/lib/mysql:/var/lib/mysql -e  MYSQL_ROOT_PASSWORD=faster12356 docker.io/mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
- 命令解释
```
# --name mysql : 容器名字叫mysql
# --net=host : 网络模式是host
# -d : 容器后台运行
# --restart always : 容器自动重启
# -v /var/lib/mysql:/var/lib/mysql : -v 容器数据卷挂载,宿主机目录:容器目录
# -e  MYSQL_ROOT_PASSWORD=faster12356 : mysql容器的root用户密码为faster12356
```
### 2.创建MySQL用户
- 进入mysql容器 `docker exec -it mysql /bin/bash`
- 用root用户连接mysql `mysql -uroot -pfaster12356`
- 创建远程登陆`faster`用户,密码是`faster2019` 
```
CREATE USER 'faster'@'%' IDENTIFIED BY 'faster2019';
```
### 3.创建和授权数据库
- 创建`db_faster`数据库
`create database db_faster default charset utf8 collate utf8_general_ci;` 
- 授权给`faster`用户
```
grant all privileges on db_faster.* to 'faster'@'localhost' identified by 'faster2019'; # 本地授权
grant all privileges on db_faster.* to 'faster'@'%' identified by 'faster2019'; #远程授权
flush privileges; # 刷新权限表,使授权生效
```
### 4.Django连接数据库设置
- 修改数据库设置`生产环境的数据库配置,路径是/FasterRunner/settings/pro.py`里面`DATABASES`字典相关配置`NAME,USER,PASSWORD,HOST`

### 5.配置和运行`RabbittMQ`(消息队列中间件)
- 运行RabbittMQ
```
rabbitmq docker run -d --name --net=host --restart always rabbitmq -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
1```
- 配置`RabbittMQ`
在`/FasterRunner/settings/base.py`修改`BROKER_URL`的`IP,username,password`

### 6.构建`fastrunner`镜像
`docker build -t fastrunner:latest .`

### 7.后台运行`fastrunner`容器,默认端口8000
`docker run -d --name fastrunner --net=host --restart always fastrunner:latest`

### 8.进入`fastrunner`容器内部
`docker exec -it fastrunner /bin/sh`

### 9.`Django`生成数据库脚本
```
# 指定--settings=FasterRunner.settings.pro文件来生成fastrunner fastuser djcelery数据库脚本
python3 manage.py makemigrations --settings=FasterRunner.settings.pro fastrunner fastuser djcelery
```

### 10.`Django`执行数据库脚本
```
# migrate for database
python3 manage.py migrate --settings=FasterRunner.settings.pro fastrunner
python3 manage.py migrate --settings=FasterRunner.settings.pro fastuser
python3 manage.py migrate --settings=FasterRunner.settings.pro djcelery
```
### 11.`Docker`相关操作
```bash
# 启动Docker
sudo systemctl start docker

# 查看日志fastrunner容器日志
docker container logs fastrunner

# 正在运行的容器
docker container ls

# 删除容器fastrunner
 docker container rm fastrunner
 
# 停止容器fastrunner
 docker container stop fastrunner

# 启动容器fastrunner
 docker container start fastrunner 

# Docker镜像
docker images

```


# 普通模式部署
- [Django原生部署](https://www.jianshu.com/p/e26ccc21ddf2)
- [uWSGI+Nginx+Supervisor+Python虚拟环境部署](https://www.jianshu.com/p/577a966b0998)