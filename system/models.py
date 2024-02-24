from django.db import models

from fastuser.models import BaseTable


# Create your models here.


class LogRecord(BaseTable):
    class Meta:
        db_table = "log_record"

    request_id = models.CharField(max_length=100, null=True, db_index=True)
    level = models.CharField(max_length=20)
    message = models.TextField(db_index=True)
