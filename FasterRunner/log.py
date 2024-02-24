# !/usr/bin/python3

# @Author: 花菜
# @File: log.py
# @Time : 2023/9/17 22:25
# @Email: lihuacai168@gmail.com

import logging


class DatabaseLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        from system.models import LogRecord  # 引入上面定义的LogRecord模型

        LogRecord.objects.create(
            request_id=record.request_id,
            level=record.levelname,
            message=self.format(record),
        )
