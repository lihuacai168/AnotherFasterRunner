[![LICENSE](https://img.shields.io/github/license/HttpRunner/FasterRunner.svg)](https://github.com/HttpRunner/FasterRunner/blob/master/LICENSE)
# FasterRunner

🚀 让接口测试更简单，让自动化更快速！

- [X] 🚀 **落地实战** - 已在 5+ 个公司中落地实战，效果显著
- [X] 🔄 **无缝同步** - 支持一键同步 YAPI（Swagger，Postman）接口数据，告别手动录入的繁琐
- [X] 💪 **强大引擎** - 基于Pythone3 + Requests 打造，轻松应对各类 HTTP(S) 测试场景，稳定可靠
- [X] 🔐 **灵活扩展** - 通过 debugtalk.py 自定义函数，轻松实现接口签名、加解密等自定义功能
- [X] 🎯 **完美联动** - 强大的 hook 机制，优雅处理接口间的token依赖和参数传递，打通测试全流程
- [X] ⏰ **智能调度** - 内置 crontab 定时任务，无学习成本，帮你实现自动化监控
- [X] 📊 **数据驱动** - 支持测试用例参数化，释放测试人员生产力
- [X] 🔄 **持续集成** - 完美对接 Gitlab-CI、Jenkins 等CI工具，助力研发效能提升
- [X] 📈 **清晰报告** - 简洁美观的测试报告，包含详尽的统计信息和日志记录，一目了然
- [X] 📱 **即时通知** - 自动推送测试报告至飞书、钉钉、企业微信，随时掌握测试动态

![](https://cdn.jsdelivr.net/gh/lihuacai168/images/img/project_detail.png)

# 📐 系统架构

```mermaid
graph TB
    %% 用户层
    subgraph "用户层"
        User[👤 测试用户]
        Browser[🌐 浏览器]
        CI[🔄 CI/CD工具<br/>Jenkins/GitLab CI]
    end

    %% 前端层
    subgraph "前端层"
        Web[📱 Vue.js Web界面<br/>端口: 80]
        Admin[⚙️ Django Admin<br/>端口: 8000]
    end

    %% 负载均衡
    subgraph "负载均衡层"
        WebNginx[🔀 Web Nginx<br/>静态资源服务]
        AdminNginx[🔀 Admin Nginx<br/>管理接口代理]
    end

    %% 应用层
    subgraph "应用服务层"
        Django[🐍 Django REST API<br/>认证/授权/业务逻辑]
        
        subgraph "核心模块"
            FastRunner[📋 FastRunner<br/>测试用例管理]
            FastUser[👥 FastUser<br/>用户管理]
            MockServer[🎭 Mock Server<br/>接口模拟]
            System[🔧 System<br/>系统监控]
        end
    end

    %% 任务调度层
    subgraph "任务调度层"
        CeleryBeat[⏰ Celery Beat<br/>定时任务调度]
        CeleryWorker[⚡ Celery Worker<br/>异步任务执行]
        HttpRunner[🏃 HttpRunner<br/>测试执行引擎]
    end

    %% 消息队列
    subgraph "消息队列"
        RabbitMQ[🐰 RabbitMQ<br/>消息代理<br/>端口: 5672/15672]
    end

    %% 数据层
    subgraph "数据存储层"
        Database[(🗄️ MariaDB/MySQL<br/>业务数据存储<br/>端口: 3306)]
        Files[📁 本地文件<br/>日志/静态资源/报告]
    end

    %% 外部服务
    subgraph "外部集成"
        YAPI[📡 YAPI接口<br/>接口同步]
        Swagger[📄 Swagger/Postman<br/>接口导入]
        Notification[📢 通知服务<br/>飞书/钉钉/企业微信]
        Email[📧 邮件服务<br/>SMTP]
        Loki[📊 Grafana Loki<br/>日志聚合]
    end

    %% 连接关系
    User --> Browser
    User --> CI
    Browser --> Web
    Browser --> Admin
    CI --> Django

    Web --> WebNginx
    Admin --> AdminNginx
    WebNginx --> Django
    AdminNginx --> Django

    Django --> FastRunner
    Django --> FastUser
    Django --> MockServer
    Django --> System
    Django --> Database

    Django --> CeleryBeat
    CeleryBeat --> RabbitMQ
    RabbitMQ --> CeleryWorker
    CeleryWorker --> HttpRunner
    HttpRunner --> Database
    HttpRunner --> Files

    Django --> YAPI
    Django --> Swagger
    CeleryWorker --> Notification
    CeleryWorker --> Email
    Django --> Loki

    %% 样式
    classDef frontend fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef database fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef queue fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef external fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class Web,Admin,WebNginx,AdminNginx frontend
    class Django,FastRunner,FastUser,MockServer,System,CeleryBeat,CeleryWorker,HttpRunner backend
    class Database,Files database
    class RabbitMQ queue
    class YAPI,Swagger,Notification,Email,Loki external
```

## 🏗️ 架构说明

### 分层架构设计

- **用户层**: 支持Web界面操作和CI/CD集成
- **前端层**: Vue.js单页应用 + Django Admin管理界面
- **负载均衡层**: Nginx反向代理，处理静态资源和API请求
- **应用服务层**: Django REST框架，模块化设计
- **任务调度层**: Celery分布式任务队列，支持定时和异步任务
- **数据存储层**: MariaDB关系数据库 + 本地文件存储（日志、报告、静态资源）

### 核心特性

- **微服务化设计**: 模块间松耦合，便于扩展维护
- **异步任务处理**: 大型测试任务异步执行，避免阻塞
- **定时调度**: 支持cron表达式的定时任务
- **容器化部署**: Docker Compose一键部署
- **横向扩展**: 支持多Worker节点扩展

# ⚠️ 注意
> python版本需要>=3.9 
> 
> 3.9, 3.10和3.11都经过测试
 
# 📚 文档
- 使用文档 https://www.yuque.com/lihuacai/fasterunner

# 🚀 Quick Start

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

# 💻 Dev
- [Django原生部署](https://www.jianshu.com/p/e26ccc21ddf2)

# 🔧 uWSGI
- [uWSGI+Nginx+Supervisor+Python虚拟环境部署](https://www.jianshu.com/p/577a966b0998)

# ⭐ Star History

![Star History Chart](https://api.star-history.com/svg?repos=lihuacai168/AnotherFasterRunner&type=Date)

# 👥 贡献者
<a href="https://github.com/lihuacai168/AnotherFasterRunner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lihuacai168/AnotherFasterRunner" />
</a>

# 🙏 鸣谢

感谢 JetBrains 对开源项目的支持

<a href="https://jb.gg/OpenSourceSupport">
  <img src="https://user-images.githubusercontent.com/8643542/160519107-199319dc-e1cf-4079-94b7-01b6b8d23aa6.png" align="left" height="150" width="150" alt="JetBrains">
</a>
