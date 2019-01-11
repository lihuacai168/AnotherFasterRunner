FROM python:3.5.6-stretch

MAINTAINER dreamyin


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]