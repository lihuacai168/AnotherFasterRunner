# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: log.py
# @Time : 2023/9/17 22:25
# @Email: lihuacai168@gmail.com

import logging
from datetime import datetime

from django.conf import settings

from FasterRunner.mycelery import app


class DatabaseLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        from system.models import LogRecord  # 引入上面定义的LogRecord模型

        LogRecord.objects.create(
            request_id=record.request_id,
            level=record.levelname,
            message=self.format(record),
        )


class LokiHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.loki_url = settings.LOKI_URL or ''
        self.loki_username = settings.LOKI_USERNAME
        self.loki_password = settings.LOKI_PASSWORD

    def emit(self, record):
        log_entry = self.format(record)
        self.send_to_loki(log_entry, record.levelname.lower(), record.request_id)

    def send_to_loki(self, log_entry, level, trace_id: str):
        if not self.loki_url or not self.loki_username or not self.loki_username:
            return
        data = {
            "streams": [
                {
                    "stream": {
                        "level": level,
                        "job": "fastrunner",
                        "traceID": trace_id,
                    },
                    "values": [
                        [str(int(datetime.now().timestamp() * 1e9)), log_entry]
                    ]
                }
            ]
        }
        try:
            kwargs = {
                'loki_url': self.loki_url, 'data': data, 'loki_username': self.loki_username,
                'loki_password': self.loki_password
            }
            app.send_task(name="system.tasks.send_log_to_loki", args=[], kwargs=kwargs)
        except Exception as e:
            logging.error(str(e))
