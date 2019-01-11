# FasterWeb+FasterRunner docker-compose部署

## 一.安装docker-compose  
```python
# pip安装docker-compose
pip install docker-compose
# 找到docker-compose安装目录   /usr/local/python37/bin/docker-compose
find / -name docker-compose
# 创建docker-compose软链接
ln -s /usr/local/python37/bin/docker-compose /usr/bin/docker-compose
```

--------

## 二.配置docker-compose.yml,FasterRunner和FasterWeb
#### 2.1 保存如下配置到docker-compose.yml  

需要自定义的配置：  

**MYSQL_ROOT_PASSWORD**为mysql root账号密码  
**/root/workspace/FasterRunner**为FasterRunner根目录  
**/root/workspace/FasterWeb**为FasterWeb根目录  

请自行设置

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

```
#### 2.2 更改FasterRunner setting.py数据库配置

PASSWORD=MYSQL_ROOT_PASSWORD  
HOST=db (docker-compose中设置的mysql容器名)

#### 2.3 更改FasterWeb配置  

* 修改default.conf配置文件 server_name的ip,注意为当前docker服务宿主机的ip地址！！！  
* 修改/src/restful/api.js baseUrl地址, 即为fastrunner容器运行的宿主机地址
* 执行npm install, npm run build # 生成生产环境包

----------
## 三.构建FasterWeb & FasterRunner镜像

在docker-compose.yml所在目录执行命令：  
```python
docker-compose build
```
-------
## 四.启动容器
在docker-compose.yml所在目录执行命令：  
```python
docker-compose up -d
```

备注：首次启动无mysql镜像时，会先pull mysql镜像再启动

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

## 六.登陆FasterRunner
open url: http://宿主机ip:8082/#/fastrunner/register

-------
备注：  
docker-compose命令：
```python
docker-compose build     # 构建镜像
docker-compose up -d     # 启动容器
docker-compose stop      # 停止容器
docker-compose restart   # 重启容器
```