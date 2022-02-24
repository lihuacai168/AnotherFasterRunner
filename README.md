# FasterRunner
- [X] 支持同步YAPI（Swagger，Postman），无需手动录入接口
- [X] 继承 Requests 的全部特性，轻松实现 HTTP(S) 的各种测试需求
- [X]  借助驱动代码（debugtalk.py），在测试脚本中轻松实现请求参数签名，加密和解密响应等
- [X]  支持完善的 hook 机制，通过请求前置和后置函数，完美解决单接口的token依赖和多个接口的参数传递
- [X]  类crontab的定时任务, 无需额外学习成本
- [X]  测试用例支持参数化和数据驱动机制
- [X]  Gitlab-CI, Jenkins 等持续集成工具完美结合
- [X]  测试结果统计报告简洁清晰，附带详尽统计信息和日志记录
- [X]  测试报告推送飞书，钉钉，企业微信等

[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/HttpRunner/FasterRunner.svg?branch=master)](https://travis-ci.org/HttpRunner/FasterRunner) ![pyversions](https://img.shields.io/pypi/pyversions/Django.svg)

# [使用文档](https://www.yuque.com/lihuacai/sggdx7/cn5ncg)

# Quick Start
## 构建前端静态文件
```shell
cd ./web
yarn install
npm run build
```
## 启动所有服务
```shell
docker-compose up --build -d
```


# Dev
- [Django原生部署](https://www.jianshu.com/p/e26ccc21ddf2)

# uWSGI
- [uWSGI+Nginx+Supervisor+Python虚拟环境部署](https://www.jianshu.com/p/577a966b0998)