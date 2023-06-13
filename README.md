# FasterRunner

[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE)
[![travis-ci](https://travis-ci.org/HttpRunner/FasterRunner.svg?branch=master)](https://travis-ci.org/HttpRunner/FasterRunner)
![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)
![screen shoot](https://cdn.jsdelivr.net/gh/lihuacai168/images/img/project_detail.png)

## Feature

- [X] 支持同步YAPI（Swagger，Postman），无需手动录入接口
- [X] 继承 Requests 的全部特性，轻松实现 HTTP(S) 的各种测试需求
- [X]  借助驱动代码（debugtalk.py），在测试脚本中轻松实现请求参数签名，加密和解密响应等
- [X]  支持完善的 hook 机制，通过请求前置和后置函数，完美解决单接口的token依赖和多个接口的参数传递
- [X]  类crontab的定时任务, 无需额外学习成本
- [X]  测试用例支持参数化和数据驱动机制
- [X]  Gitlab-CI, Jenkins 等持续集成工具完美结合
- [X]  测试结果统计报告简洁清晰，附带详尽统计信息和日志记录
- [X]  测试报告推送飞书，钉钉，企业微信等

## 注意

> 支持`python3.9-python3.11`版本
>
> `V2`版本使用`django-celery-beat`代替`djcelery`, 需要手动执行sql文件夹中的`django_celery_beat_init.sql`

## [使用文档](https://www.yuque.com/lihuacai/fasterunner)

- 使用文档 <https://www.yuque.com/lihuacai/fasterunner>

## Quick Start

- 开发环境准备：mysql
- 启动mysql后执行初始化脚本：db目录中两个脚本

```shell
docker pull mysql:5.7
docker run --name mysql -v ./mysql:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest
```

## 正式部署

```shell
# 编辑Dockerfile，安装必要的依赖及确定WORKDIR
apk add Nginx
...
WORKDIR /app/
```

```shell
# 单独构建app及web应用，分别在AnotherFasterRunner及./FasterWeb目录下
cd ./ComposeDeploy
docker build -t registry-vpc.cn-hangzhou.aliyuncs.com/cbk/fasterrunner:base-latest .
cd ..
docker build -t registry-vpc.cn-hangzhou.aliyuncs.com/cbk/fasterrunner:app-latest .
cd ./web
npm config set registry https://registry.npmmirror.com
npm install -g pnpm
pnpm install
pnpm build
docker build -t registry-vpc.cn-hangzhou.aliyuncs.com/cbk/fasterrunner:web-latest .
```

```shell
# 设置环境变量
cp .env.example $HOME/.env

# 使用makefile命令快速启动所有服务，没错，一个命令就搞定
cd AnotherFasterRunner && make

# 或者使用docker-compose原始的命令, 指定配置文件启动
cd AnotherFasterRunner && docker-compose -f docker-compose-for-fastup.yml --env-file .env.example up -d
```

```shell
# 使用makefile命令快速启动
make up

# 或者使用docker-compose原始的命令, 指定配置文件启动, .env是绝对路径
docker-compose --env-file=$HOME/.env up --build -d
```

## Dev

- [Django原生部署](https://www.jianshu.com/p/e26ccc21ddf2)

## uWSGI

- [uWSGI+Nginx+Supervisor+Python虚拟环境部署](https://www.jianshu.com/p/577a966b0998)

## Nginx配置

```shell
#1、验证配置文件

/usr/local/nginx/sbin/nginx -tc /usr/local/nginx/conf/nginx.conf

or

/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf

#2、指定配置文件启动

/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf

#3、指定配置文件重启

/usr/local/nginx/sbin/nginx -s reload -c /usr/local/nginx/conf/nginx.conf

# 注：/usr/local/nginx/ 目录视自己的安装情况而定。配置文件同样根据自己的命名习惯指定
# ————————————————
# 版权声明：本文为CSDN博主「gblfy」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/weixin_40816738/article/details/121512708
```

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=lihuacai168/AnotherFasterRunner&type=Date)

## 贡献者

![![contributors](https://github.com/lihuacai168/AnotherFasterRunner/graphs/contributors)](https://contrib.rocks/image?repo=lihuacai168/AnotherFasterRunner)

## 鸣谢

感谢 JetBrains 对开源项目的支持

<a href="https://jb.gg/OpenSourceSupport">
  <img src="https://user-images.githubusercontent.com/8643542/160519107-199319dc-e1cf-4079-94b7-01b6b8d23aa6.png" align="left" height="150" width="150" alt="JetBrains">
</a>
