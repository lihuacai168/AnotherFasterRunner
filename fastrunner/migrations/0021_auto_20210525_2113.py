# Generated by Django 2.2 on 2021-05-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fastrunner", "0020_auto_20210525_1844"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="ci_job_id",
            field=models.CharField(
                db_index=True, default=None, max_length=15, null=True, unique=True, verbose_name="gitlab的项目id"
            ),
        ),
        migrations.AddField(
            model_name="report",
            name="ci_project_id",
            field=models.IntegerField(db_index=True, default=0, verbose_name="gitlab的项目id"),
        ),
    ]
