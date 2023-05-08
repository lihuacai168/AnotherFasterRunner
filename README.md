最近找工作（已经离职状态）:sob:   
看广深的测开机会  
个人简介：
- 普通全日制本科，8年经验，在虾皮，TCL，广州致景等工作过
- 擅长：Python，Vue，MySQL，Docker，Linux Shell
- 略懂：Go，Kafka，Redis，MQTT，大数据相关
- 弱项：Java，移动端（有ChatGPT Plus加持，我想这不是什么问题）

各位大佬招人或者内推，扫描二维码，带走我  
<img src="https://img.huacai.one/image-20230412095031719.webp" alt="image-20230412095031719" style="zoom:10%;" />


[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE)
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

![](https://cdn.jsdelivr.net/gh/lihuacai168/images/img/project_detail.png)


# 注意
> 只能使用`python3.9`版本
 
# 文档
- 使用文档 https://www.yuque.com/lihuacai/fasterunner

# Quick Start

## 拉取代码和启动服务
```shell
# 拉取代码
git clone git@github.com:lihuacai168/AnotherFasterRunner.git AnotherFasterRunner

# 如果你的机器连接不上Github，可以用国内的Gitee
# git clone git@gitee.com:lihuacai/AnotherFasterRunner.git AnotherFasterRunner

# 使用makefile命令快速启动所有服务，没错，一个命令就搞定
cd AnotherFasterRunner && make

# 或者使用docker-compose原始的命令, 指定配置文件启动
cd AnotherFasterRunner && docker-compose -f docker-compose-for-fastup.yml --env-file .env.example up -d
```

## 访问服务
```shell
# 默认是80端口，如果80端口被占用，修改env文件中的WEB_PORT即可
浏览器打开:
http://你的ip/fastrunner/login

用户:test
密码:test2020
```

# Dev
- [Django原生部署](https://www.jianshu.com/p/e26ccc21ddf2)

# uWSGI
- [uWSGI+Nginx+Supervisor+Python虚拟环境部署](https://www.jianshu.com/p/577a966b0998)

# Star History

![Star History Chart](https://api.star-history.com/svg?repos=lihuacai168/AnotherFasterRunner&type=Date)



# 贡献者
<a href="https://github.com/lihuacai168/AnotherFasterRunner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lihuacai168/AnotherFasterRunner" />
</a>

# 鸣谢

感谢 JetBrains 对开源项目的支持

<a href="https://jb.gg/OpenSourceSupport">
  <img src="https://user-images.githubusercontent.com/8643542/160519107-199319dc-e1cf-4079-94b7-01b6b8d23aa6.png" align="left" height="150" width="150" alt="JetBrains">
</a>
