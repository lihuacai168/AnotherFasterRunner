# Generated by Django 4.1.13 on 2024-02-27 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mock", "0002_alter_mockapi_options_alter_mockapi_project"),
    ]

    operations = [
        migrations.AddField(
            model_name="mockapi",
            name="api_desc",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="mockapi",
            name="api_id",
            field=models.CharField(default="4e9eb9a68bd8441d9c503f1347f156ff", max_length=32, unique=True),
        ),
        migrations.AddField(
            model_name="mockapi",
            name="api_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="mockapi",
            name="followers",
            field=models.JSONField(blank=True, default=list, null=True, verbose_name="关注者"),
        ),
        migrations.AlterField(
            model_name="mockapi",
            name="project",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="mock_apis",
                to="mock.mockproject",
                to_field="project_id",
            ),
        ),
    ]