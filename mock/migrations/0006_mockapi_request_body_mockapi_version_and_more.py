# Generated by Django 4.1.13 on 2024-03-15 01:18

from django.db import migrations, models
import mock.models


class Migration(migrations.Migration):

    dependencies = [
        ("mock", "0005_mockapilog_request_id_alter_mockapi_api_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mockapi",
            name="request_body",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="mockapi",
            name="version",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="mockapi",
            name="api_id",
            field=models.CharField(
                default=mock.models.generate_uuid, max_length=32, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="mockapi",
            name="api_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="mockapi",
            name="response_text",
            field=models.TextField(
                default='\ndef execute(req, resp):\n    import requests\n\n    url = "http://localhost:8000/api/mock/mock_api/"\n\n    payload = {}\n    headers = {\n        "accept": "application/json",\n        "X-CSRFToken": "fk5wQDlKC6ufRjk7r38pfbqyq7mTtyc5NUUqkFN5lbZf6nyHVSbAUVoqbwaGcQHT",\n    }\n\n    response = requests.request("GET", url, headers=headers, data=payload)\n    resp.data = response.json()\n'
            ),
        ),
        migrations.AlterField(
            model_name="mockapilog",
            name="request_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default=mock.models.generate_uuid,
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="mockproject",
            name="project_id",
            field=models.CharField(
                default=mock.models.generate_uuid, max_length=100, unique=True
            ),
        ),
    ]