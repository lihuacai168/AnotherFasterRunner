# FasterWeb

![LICENSE](https://img.shields.io/github/license/yinquanwang/FasterRunner.svg)
> FasterWeb that depends FasterRunner

## 本地开发环境部署

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

```

测试
-----------

1. open url(recommend chrome): http://localhost:8080/fastrunner/login

## Docker 部署 nginx模式
--------------
1. 修改default.conf配置文件 server_name的ip(宿主机IP), 端口默认8080
2. 修改/src/restful/api.js baseUrl地址, 即为fastrunner容器运行的宿主机地址
3. 执行npm install, npm run build # 生成生产环境包
3. docker build -t fasterweb:latest .    # 构建docker镜像
4. docker run -d --name fasterweb --net=host --restart always fasterweb:latest  # 后台运行docker容器
5. open url: http://宿主机ip:8080/fastrunner/login
