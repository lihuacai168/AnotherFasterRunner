# Generated by Django 4.1.13 on 2024-03-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock', '0004_remove_mockapi_followers_mockapi_enabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockapilog',
            name='request_id',
            field=models.CharField(blank=True, db_index=True, default='bc73e83696024977b002016c6ebd9967', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mockapi',
            name='api_id',
            field=models.CharField(default='28ee07527bf8431c955fdeaeb6f1626e', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='mockapilog',
            name='request_obj',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='mockapilog',
            name='response_obj',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]