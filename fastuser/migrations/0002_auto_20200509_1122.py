# Generated by Django 2.2 on 2020-05-09 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fastuser", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="phone",
            field=models.CharField(max_length=11, unique=True, verbose_name="手机号码"),
        ),
    ]
