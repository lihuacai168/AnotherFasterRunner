# Generated by Django 2.2 on 2020-10-13 10:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fastrunner", "0011_auto_20201012_2355"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="visit",
            name="times",
        ),
        migrations.AddField(
            model_name="visit",
            name="create_time",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name="创建时间"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="visit",
            name="request_body",
            field=models.TextField(default=django.utils.timezone.now, verbose_name="请求体"),
            preserve_default=False,
        ),
    ]
