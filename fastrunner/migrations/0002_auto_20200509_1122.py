# Generated by Django 2.2 on 2020-05-09 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fastrunner", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casestep",
            name="case",
            field=models.ForeignKey(
                db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to="fastrunner.Case"
            ),
        ),
    ]
