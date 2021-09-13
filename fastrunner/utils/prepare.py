import json

import pydash
import requests
from django.core.cache import cache
from django.db.models import Sum, Count, Q
from django.db.models.functions import Concat
from loguru import logger

from fastrunner import models
from fastrunner.utils.day import get_day, get_week, get_month
from fastrunner.utils.parser import Format
from djcelery import models as celery_models


def get_counter(model, pk=None):
    """
    统计相关表长度
    """
    if pk:
        return model.objects.filter(project__id=pk).count()
    else:
        return model.objects.count()


def report_status_count(pk):
    query_set = models.Report.objects.filter(project__id=pk)
    report_fail = query_set.filter(status=0).count()
    report_success = query_set.filter(status=1).count()
    return report_fail, report_success


def get_recent_date(date_type):
    if date_type == "day":
        return [get_day(n) for n in range(-5, 1)]
    elif date_type == "week":
        return [get_week(n) for n in range(-5, 1)]
    elif date_type == "month":
        return [get_month(n) for n in range(-5, 1)]


def list2dict(arr):
    keys = []
    values = []
    for d in arr:
        keys.append(str(d.get('create_time')))
        values.append(d.get('counts'))
    return dict(zip(keys, values))


def complete_list(arr, date_type):
    # {日期: 数量}
    mapping = list2dict(arr)
    date_list = get_recent_date(date_type)
    count = [mapping.get(d, 0) for d in date_list]
    return count


def get_sql_dateformat(date_type):
    if date_type == "week":
        create_time = "YEARWEEK(create_time,'%%Y-%%m-%%d')"
    elif date_type == "month":
        create_time = "DATE_FORMAT(create_time,'%%Y%%m')"
    elif date_type == "day":
        create_time = "DATE_FORMAT(create_time,'%%Y-%%m-%%d')"
    return create_time


def get_project_api_cover(project_id):
    """"""
    case_steps = models.CaseStep.objects.filter(case__project_id=project_id).filter(
        ~Q(method='config')).values('url', 'method').annotate(url_method=Concat('url', 'method'))
    return case_steps.aggregate(Count('url_method', distinct=True))


def get_project_apis(project_id) -> dict:
    """统计项目中手动创建和从yapi导入的接口数量
    """
    query = models.API.objects.filter(delete=0).filter(~Q(tag=4))
    if project_id:
        query = query.filter(project_id=project_id)

    project_api_map: dict = query.aggregate(用户创建=Count('pk', filter=~Q(creator='yapi')),
                                            yapi导入=Count('pk', filter=Q(creator='yapi')))
    return list(project_api_map.keys()), list(project_api_map.values())


def aggregate_apis_bydate(date_type, is_yapi=False) -> dict:
    """按照日，周，月统计项目中手动创建和从yapi导入的接口数量
    """
    create_time = get_sql_dateformat(date_type)

    query = models.API.objects.filter(~Q(tag=4))
    if is_yapi:
        query = query.filter(creator='yapi')
    else:
        query = query.filter(~Q(creator='yapi'))

    count_data: dict = query.extra(select={"create_time": create_time}) \
        .values('create_time', ) \
        .annotate(counts=Count('id')) \
        .values('create_time', 'counts')

    # 查询结果是按照时间升序，取最后6条
    # 没有的补0
    count = complete_list(count_data, date_type)

    return count


def aggregate_case_by_tag(project_id):
    """按照分类统计项目中的用例"""
    query = models.Case.objects
    if project_id:
        query = query.filter(project_id=project_id)
    case_count: dict = query.aggregate(冒烟用例=Count('pk', filter=Q(tag=1)),
                                       集成用例=Count('pk', filter=Q(tag=2)),
                                       监控脚本=Count('pk', filter=Q(tag=3)),
                                       核心用例=Count('pk', filter=Q(tag=4)),
                                       )
    return list(case_count.keys()), list(case_count.values())


def aggregate_reports_by_type(project_id):
    """按照类型统计项目中的报告"""
    query = models.Report.objects
    if project_id:
        query = query.filter(project_id=project_id)
    report_count: dict = query.aggregate(调试=Count('pk', filter=Q(type=1)),
                                         异步=Count('pk', filter=Q(type=2)),
                                         定时=Count('pk', filter=Q(type=3)),
                                         部署=Count('pk', filter=Q(type=4)),
                                         )
    return list(report_count.keys()), list(report_count.values())


def aggregate_reports_by_status(project_id):
    """按照状态统计项目中的报告"""
    query = models.Report.objects
    if project_id:
        query = query.filter(project_id=project_id)
    report_count: dict = query.aggregate(失败=Count('pk', filter=Q(status=0)),
                                         成功=Count('pk', filter=Q(status=1)),
                                         )
    return list(report_count.keys()), list(report_count.values())


def aggregate_reports_or_case_bydate(date_type, model):
    """按月和周统计报告创建数量"""
    create_time = get_sql_dateformat(date_type)
    qs = model.objects.extra(select={"create_time": create_time}) \
        .values('create_time', ) \
        .annotate(counts=Count('id')) \
        .values('create_time', 'counts')

    qs = list(qs)
    complete_list(qs, date_type)

    # 查询结果是按照时间升序，取最后6条
    # 没有的补0
    values = complete_list(qs, date_type)

    return values


def get_daily_count(project_id, model_name, start, end):
    # 生成日期list, ['08-12', '08-13', ...]
    recent_days = [get_day(n)[5:] for n in range(start, end)]
    models_mapping = {
        'api': models.API,
        'case': models.Case,
        'report': models.Report
    }
    model = models_mapping[model_name]
    query = model.objects
    if model_name == 'api':
        query = query.filter(~Q(tag=4))

    # 统计给定日期范围内，每天创建的条数
    count_data: list = query.filter(project_id=project_id, create_time__range=[get_day(start), get_day(end)]) \
        .extra(select={"create_time": "DATE_FORMAT(create_time,'%%m-%%d')"}) \
        .values('create_time') \
        .annotate(counts=Count('id')) \
        .values('create_time', 'counts')
    # list转dict, key是日期, value是统计数
    create_time_count_mapping = {data['create_time']: data["counts"] for data in count_data}

    # 日期为空的key，补0
    count = [create_time_count_mapping.get(d, 0) for d in recent_days]
    return {'days': recent_days, 'count': count}


def get_project_daily_create(project_id):
    """项目每天创建的api, case, report"""
    start = -6
    end = 1
    count_mapping = {}
    for model in ('api', 'case', 'report'):
        count_mapping[model] = get_daily_count(project_id, model, start, end)
    return count_mapping


def get_project_detail_v2(pk):
    """统计项目api, case, report总数和每日创建"""
    api_create_type, api_create_type_count = get_project_apis(pk)
    case_tag, case_tag_count = aggregate_case_by_tag(pk)
    report_type, report_type_count = aggregate_reports_by_type(pk)
    daily_create_count = get_project_daily_create(pk)
    res = {
        "api_count_by_create_type": {
            "type": api_create_type,
            "count": api_create_type_count
        },
        "case_count_by_tag": {
            "tag": case_tag,
            "count": case_tag_count
        },
        "report_count_by_type": {
            'type': report_type,
            'count': report_type_count
        },
        "daily_create_count": daily_create_count
    }
    return res


def get_jira_core_case_cover_rate(pk) -> dict:
    project_obj = models.Project.objects.get(pk=pk)
    jira_cases = []
    if project_obj.jira_bearer_token == '' or project_obj.jira_project_key == '':
        logger.info('jira token或者jira project key没配置')
    else:
        base_url = 'https://jira.szzhijing.com/rest/api/latest/search'
        data = {
            "jql": f"project = {project_obj.jira_project_key} AND issuetype = '测试用例'",
            "maxResults": -1
        }
        headers = {
            'Authorization': f'Bearer {project_obj.jira_bearer_token}',
            'Content-Type': 'application/json',
        }
        try:
            # TODO 分页查找所有的核心case
            res = requests.post(url=base_url, headers=headers, data=json.dumps(data)).json()
            err = res.get('errorMessages')
            if err:
                logger.error(err)
            else:
                jira_cases.extend(res['issues'])
        except Exception as e:
            logger.error(str(e))

    jira_core_case_count = 0
    for case in jira_cases:
        if pydash.get(case, 'fields.customfield_11400.value') == '是':
            jira_core_case_count += 1

    covered_case_count = len(models.Case.objects.filter(project=pk, tag=4))

    if jira_core_case_count == 0:
        core_case_cover_rate = '0.00'
    else:
        core_case_cover_rate = '%.2f' % ((covered_case_count / jira_core_case_count) * 100)

    return {
        'jira_core_case_count': jira_core_case_count,
        'core_case_count': covered_case_count,
        'core_case_cover_rate':  core_case_cover_rate
    }


def get_project_detail(pk):
    """
    项目详细统计信息
    """

    api_count = get_counter(models.API, pk=pk)
    case_count = get_counter(models.Case, pk=pk)
    config_count = get_counter(models.Config, pk=pk)
    variables_count = get_counter(models.Variables, pk=pk)
    report_count = get_counter(models.Report, pk=pk)
    report_fail, report_success = report_status_count(pk=pk)
    host_count = get_counter(models.HostIP, pk=pk)
    # plan_count = get_counter(models.Plan, pk=pk)
    task_query_set = celery_models.PeriodicTask.objects.filter(description=pk)
    task_count = task_query_set.count()
    case_id = []
    task_query_set = task_query_set.filter(enabled=1).values("args")
    for i in task_query_set:
        case_id += eval(i.get('args'))
    case_step_count = models.Case.objects.filter(pk__in=case_id).aggregate(Sum("length"))

    return {
        "api_count": api_count,
        "case_count": case_count,
        "task_count": task_count,
        "config_count": config_count,
        "variables_count": variables_count,
        "report_count": report_count,
        "report_fail": report_fail,
        "report_success": report_success,
        "host_count": host_count,
        "case_step_count": case_step_count.get("length__sum"),
    }


def project_init(project):
    """新建项目初始化
    """

    # 自动生成默认debugtalk.py
    models.Debugtalk.objects.create(project=project)
    # 自动生成API tree
    models.Relation.objects.create(project=project)
    # 自动生成Test Tree
    models.Relation.objects.create(project=project, type=2)


def project_end(project):
    """删除项目相关表 filter不会报异常 最好不用get
    """
    models.Debugtalk.objects.filter(project=project).delete()
    models.Config.objects.filter(project=project).delete()
    models.API.objects.filter(project=project).delete()
    models.Relation.objects.filter(project=project).delete()
    models.Report.objects.filter(project=project).delete()
    models.Variables.objects.filter(project=project).delete()
    celery_models.PeriodicTask.objects.filter(description=project).delete()

    case = models.Case.objects.filter(project=project).values_list('id')

    for case_id in case:
        models.CaseStep.objects.filter(case__id=case_id).delete()


def tree_end(params, project):
    """
    project: Project Model
    params: {
        node: int,
        type: int
    }
    """
    type = params['type']
    node = params['node']

    if type == 1:
        models.API.objects. \
            filter(relation=node, project=project).delete()

    # remove node testcase
    elif type == 2:
        case = models.Case.objects. \
            filter(relation=node, project=project).values('id')

        for case_id in case:
            models.CaseStep.objects.filter(case__id=case_id['id']).delete()
            models.Case.objects.filter(id=case_id['id']).delete()


def update_casestep(body, case, username):
    step_list = list(models.CaseStep.objects.filter(case=case).values('id'))

    for index in range(len(body)):

        test = body[index]
        try:
            format_http = Format(test['newBody'])
            format_http.parse()
            name = format_http.name
            new_body = format_http.testcase
            url = format_http.url
            method = format_http.method

        except KeyError:
            if 'case' in test.keys():
                case_step = models.CaseStep.objects.get(id=test['id'])
            elif test["body"]["method"] == "config":
                case_step = models.Config.objects.get(name=test['body']['name'])
            else:
                case_step = models.API.objects.get(id=test['id'])

            new_body = eval(case_step.body)
            name = test['body']['name']

            if case_step.name != name:
                new_body['name'] = name

            if test["body"]["method"] == "config":
                url = ""
                method = "config"
                # config没有source_api_id,默认为0
                source_api_id = 0
            else:
                url = test['body']['url']
                method = test['body']['method']
                source_api_id = test.get('source_api_id', 0)
                # 新增的case_step没有source_api_id字段,需要重新赋值
                if source_api_id == 0:
                    source_api_id = test['id']

        kwargs = {
            "name": name,
            "body": new_body,
            "url": url,
            "method": method,
            "step": index,
            "source_api_id": source_api_id
        }
        # is_copy is True表示用例步骤是复制的
        if 'case' in test.keys() and test.pop("is_copy", False) is False:
            models.CaseStep.objects.filter(id=test['id']).update(**kwargs, updater=username)
            step_list.remove({"id": test['id']})
        else:
            kwargs['case'] = case
            models.CaseStep.objects.create(**kwargs, creator=username)

    #  去掉多余的step
    for content in step_list:
        models.CaseStep.objects.filter(id=content['id']).delete()


def generate_casestep(body, case, username):
    """
    生成用例集步骤
    [{
        id: int,
        project: int,
        name: str,
        method: str,
        url: str
    }]

    """
    #  index也是case step的执行顺序
    case_steps: list = []
    for index in range(len(body)):

        test = body[index]
        try:
            format_http = Format(test['newBody'])
            format_http.parse()
            name = format_http.name
            new_body = format_http.testcase
            url = format_http.url
            method = format_http.method

        except KeyError:
            if test["body"]["method"] == "config":
                name = test["body"]["name"]
                method = test["body"]["method"]
                config = models.Config.objects.get(name=name)
                url = config.base_url
                new_body = eval(config.body)
                source_api_id = 0  # config没有api,默认为0
            else:
                api = models.API.objects.get(id=test['id'])
                new_body = eval(api.body)
                name = test['body']['name']

                if api.name != name:
                    new_body['name'] = name

                url = test['body']['url']
                method = test['body']['method']
                source_api_id = test['id']
        kwargs = {
            "name": name,
            "body": new_body,
            "url": url,
            "method": method,
            "step": index,
            "case": case,
            "source_api_id": source_api_id,
            "creator": username
        }
        case_step = models.CaseStep(**kwargs)
        case_steps.append(case_step)
    models.CaseStep.objects.bulk_create(objs=case_steps)


def case_end(pk):
    """
    pk: int case id
    """
    # models.CaseStep.objects.filter(case__id=pk).delete()
    if isinstance(pk, int):
        models.Case.objects.filter(id=pk).delete()
    elif isinstance(pk, list):
        models.Case.objects.filter(id__in=pk).delete()
    else:
        return
