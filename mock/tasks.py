# tasks.py
from celery import shared_task
from mock.models import MockAPILog


@shared_task
def log_mock_api(request_obj, request_id, api_id, project_id, req_time, response_obj):
    log_obj = MockAPILog.objects.create(
        request_obj=request_obj,
        request_id=request_id,
        api_id=api_id,
        project_id=project_id,
        create_time=req_time
    )
    log_obj.response_obj = response_obj
    log_obj.save()
    return log_obj.id
