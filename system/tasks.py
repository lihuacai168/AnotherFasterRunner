import json

from celery import shared_task
from requests.auth import HTTPBasicAuth

import requests


@shared_task
def send_log_to_loki(*args, **kwargs):
    url = kwargs['loki_url']
    loki_username = kwargs['loki_username']
    loki_password = kwargs['loki_password']
    auth = HTTPBasicAuth(username=loki_username, password=loki_password)
    data = kwargs['data']
    headers = {
        'Content-Type': 'application/json'
    }
    requests.post(url, headers=headers, data=json.dumps(data), auth=auth)
