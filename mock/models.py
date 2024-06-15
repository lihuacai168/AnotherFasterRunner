import random
import string
import time
import uuid

from django.db import models
from fastuser.models import BaseTable


def generate_uuid():
    return uuid.uuid4().hex


def generate_short_id():
    timestamp = int(time.time() * 1000)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f'{timestamp}{random_string}'


class MockProject(BaseTable):
    project_id = models.CharField(max_length=100, unique=True, default=generate_short_id)
    project_name = models.CharField(max_length=100)
    project_desc = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "mock项目表"
        db_table = "mock_project_tab"
        unique_together = ["project_id"]


resp_text = """
def execute(req, resp):
    import requests

    url = "http://localhost:8000/api/mock/mock_api/"

    payload = {}
    headers = {
        "accept": "application/json",
        "X-CSRFToken": "fk5wQDlKC6ufRjk7r38pfbqyq7mTtyc5NUUqkFN5lbZf6nyHVSbAUVoqbwaGcQHT",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp.data = response.json()
"""


class MockAPI(BaseTable):
    METHOD_CHOICES = [
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
        ("PATCH", "PATCH"),
    ]

    project = models.ForeignKey(
        MockProject,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        blank=True,
        null=True,
        to_field="project_id",
        related_name="mock_apis",
    )
    request_path = models.CharField(max_length=100)
    request_method = models.CharField(
        max_length=10, choices=METHOD_CHOICES, default="POST"
    )
    request_body = models.JSONField(default=dict, blank=True, null=True)
    response_text = models.TextField(default=resp_text)
    is_active = models.BooleanField(default=True)

    api_name = models.CharField(max_length=100)
    api_desc = models.CharField(max_length=100, null=True, blank=True)
    # uuid hex
    api_id = models.CharField(max_length=32, default=generate_uuid, unique=True)
    enabled = models.BooleanField(default=True)

    # 添加version字段用于乐观锁控制
    version = models.IntegerField(default=1)  # 新增版本字段，默认值为1

    # TODO 改成many to many
    # followers: list = models.JSONField(null=True, blank=True, default=[], verbose_name="关注者")

    class Meta:
        verbose_name = "mock接口表"
        db_table = "mock_api_tab"
        unique_together = ["project", "request_path", "request_method"]
        ordering = ["-create_time"]


class MockAPILog(BaseTable):
    api = models.ForeignKey(
        MockAPI,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        to_field="api_id",
        related_name="logs",
    )
    project = models.ForeignKey(
        MockProject,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        blank=True,
        null=True,
        to_field="project_id",
        related_name="mock_logs",
    )
    request_obj = models.JSONField(default=dict, blank=True)
    response_obj = models.JSONField(default=dict, null=True, blank=True)
    request_id = models.CharField(
        max_length=100, default=generate_uuid, db_index=True, null=True, blank=True
    )

    class Meta:
        verbose_name = "mock api log表"
        db_table = "mock_api_log"
        ordering = ["-create_time"]
