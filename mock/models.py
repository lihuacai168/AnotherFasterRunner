import uuid

from django.db import models

from fastuser.models import BaseTable


class MockProject(BaseTable):
    project_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=100)
    project_desc = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "mock项目表"
        db_table = "mock_project_tab"
        unique_together = ["project_id"]


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
    request_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default="POST")
    response_text = models.TextField()
    is_active = models.BooleanField(default=True)

    api_name = models.CharField(max_length=100, null=True, blank=True)
    api_desc = models.CharField(max_length=100, null=True, blank=True)
    # uuid hex
    api_id = models.CharField(max_length=32, default=uuid.uuid4().hex, unique=True)
    # TODO 改成many to many
    followers: list = models.JSONField(null=True, blank=True, default=[], verbose_name="关注者")
    models.ManyToManyField

    class Meta:
        verbose_name = "mock接口表"
        db_table = "mock_api_tab"
        unique_together = ["project", "request_path", "request_method"]
        ordering = ["-create_time"]
