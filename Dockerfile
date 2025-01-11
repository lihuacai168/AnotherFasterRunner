# 使用 python:3.11-buster 作为基础镜像
FROM python:3.11-buster as Base

# 安装 Poetry
RUN pip install poetry==1.8.5

# 复制 pyproject.toml 和 poetry.lock 文件
COPY pyproject.toml poetry.lock ./

# 使用 Poetry 生成 requirements.txt 文件
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 安装依赖
ARG DEBIAN_REPO="deb.debian.org"
ARG PIP_INDEX_URL="https://pypi.org/simple"

RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y python3-dev build-essential netcat-openbsd libpcre3-dev libldap2-dev libsasl2-dev && \
    pip install -r requirements.txt -i ${PIP_INDEX_URL} && \
    apt-get remove -y python3-dev build-essential libpcre3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 使用 python:3.11-buster 作为基础镜像
FROM python:3.11-buster
ENV TZ=Asia/Shanghai

# 设置时区
ARG DEBIAN_REPO="deb.debian.org"
RUN echo "deb http://$DEBIAN_REPO/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://$DEBIAN_REPO/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖
COPY --from=Base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 设置权限
RUN chmod +x /app/start.sh

# 收集静态文件
RUN python manage.py collectstatic --settings=FasterRunner.settings.docker --no-input

# 设置入口点
ENTRYPOINT ["/app/start.sh"]
