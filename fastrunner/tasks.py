import logging

from celery import Task, shared_task
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import PeriodicTask

from fastrunner import models
from fastrunner.utils import lark_message
from fastrunner.utils.ding_message import DingMessage
from fastrunner.utils.loader import debug_api, debug_suite, save_summary
from fastrunner.utils.safe_json_parser import safe_json_loads

log = logging.getLogger(__name__)


def update_task_total_run_count(task_id):
    if task_id:
        task = PeriodicTask.objects.get(id=task_id)
        total_run_count = task.total_run_count + 1
        dt = task.date_changed
        PeriodicTask.objects.filter(id=task_id).update(date_changed=dt, total_run_count=total_run_count)


class MyBaseTask(Task):
    def run(self, *args, **kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_task_total_run_count(kwargs.get("task_id"))

    def on_success(self, retval, task_id, args, kwargs):
        update_task_total_run_count(kwargs.get("task_id"))


@shared_task
def async_debug_api(api, project, name, config=None):
    """异步执行api"""
    summary = debug_api(api, project, config=config, save=False)
    save_summary(name, summary, project)


@shared_task
def async_debug_suite(suite, project, obj, report, config, user=""):
    """异步执行suite"""
    summary, _ = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(name=report, summary=summary, project=project, type=2, user=user)


@shared_task(base=MyBaseTask)
def schedule_debug_suite(*args, **kwargs):
    """定时任务"""

    project = kwargs["project"]
    suite = []
    test_sets = []
    config_list = []
    for pk in args:
        try:
            name = models.Case.objects.get(id=pk).name
            suite.append({"name": name, "id": pk})
        except ObjectDoesNotExist:
            pass
    override_config = kwargs.get("config", "")
    override_config_body = None
    if override_config and override_config != "请选择":
        override_config_body = safe_json_loads(
            models.Config.objects.get(name=override_config, project__id=project).body
        )

    for content in suite:
        test_list = models.CaseStep.objects.filter(case__id=content["id"]).order_by("step").values("body")

        testcase_list = []
        config = None
        for content in test_list:
            body = safe_json_loads(content["body"])
            if "base_url" in body["request"].keys():
                if override_config_body:
                    config = override_config_body
                    continue
                config = safe_json_loads(models.Config.objects.get(name=body["name"], project__id=project).body)
                continue
            testcase_list.append(body)
        config_list.append(config)
        test_sets.append(testcase_list)

    is_parallel = kwargs.get("is_parallel", False)
    summary, _ = debug_suite(test_sets, project, suite, config_list, save=False, allow_parallel=is_parallel)
    task_name = kwargs["task_name"]

    if kwargs.get("run_type") == "deploy":
        task_name = "部署_" + task_name
        report_type = 4
    else:
        report_type = 3

    report_id = save_summary(task_name, summary, project, type=report_type, user=kwargs.get("user", ""))

    strategy = kwargs["strategy"]
    if strategy == "始终发送" or (strategy == "仅失败发送" and summary["stat"]["failures"] > 0):
        webhook = kwargs.get("webhook", "")
        log.info(f"开始发送消息, {webhook=}")
        DING_OPEN_API: str = "https://oapi.dingtalk.com"
        FEISHU_OPEN_API: str = "https://open.feishu.cn"

        if webhook.startswith(DING_OPEN_API) is False and webhook.startswith(FEISHU_OPEN_API) is False:
            log.warning(f"{webhook=}还不支持, 目前仅支持钉钉和飞书")

        if webhook.startswith(DING_OPEN_API):
            log.info("开始发送钉钉消息")
            ding_message = DingMessage(webhook=webhook)
            # log.info(f'{summary=}, {task_name=}')
            ding_message.send_ding_msg(summary)
            log.info("发送钉钉消息完成")

        if webhook.startswith(FEISHU_OPEN_API):
            log.info("开始发送飞书消息")
            summary["task_name"] = task_name
            summary["report_id"] = report_id
            lark_message.send_message(summary=summary, webhook=webhook, case_count=len(args))
            log.info("发送飞书消息完成")
