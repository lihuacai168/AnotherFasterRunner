from fastrunner import models
from fastrunner.utils.parser import Format


def get_counter(model, pk=None):
    """
    统计相关表长度
    """
    if pk:
        return model.objects.filter(project__id=pk).count()
    else:
        return model.objects.count()


def get_project_detail(pk):
    """
    项目详细统计信息
    """
    api_count = get_counter(models.API, pk=pk)
    case_count = get_counter(models.Case, pk=pk)
    team_count = get_counter(models.Team, pk=pk)
    config_count = get_counter(models.Config, pk=pk)
    variables_count = get_counter(models.Variables, pk=pk)
    report_count = get_counter(models.Report, pk=pk)

    return {
        "api_count": api_count,
        "case_count": case_count,
        "team_count": team_count,
        "config_count": config_count,
        "variables_count": variables_count,
        "report_count": report_count
    }


def project_init(project):
    """
    新建项目初始化
    """
    tree = [{
        "id": 1,
        "label": "默认分组",
        "children": []
    }]
    # 自动生成默认debugtalk.py
    models.Debugtalk.objects.create(project=project)
    # 自动生成API tree
    models.Relation.objects.create(project=project, tree=tree)
    # 自动生成Test Tree
    models.Relation.objects.create(project=project, type=2, tree=tree)


def project_end(project):
    """
    删除项目相关表 filter不会报异常 最好不用get
    """
    models.Debugtalk.objects.filter(project=project).delete()
    models.Team.objects.filter(project=project).delete()
    models.Config.objects.filter(project=project).delete()
    models.API.objects.filter(project=project).delete()
    models.Relation.objects.filter(project=project).delete()
    models.Report.objects.filter(project=project).delete()
    models.Variables.objects.filter(project=project).delete()

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


def update_casestep(body, case):
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
            else:
                url = test['body']['url']
                method = test['body']['method']

        kwargs = {
            "name": name,
            "body": new_body,
            "url": url,
            "method": method,
            "step": index,
        }
        if 'case' in test.keys():
            models.CaseStep.objects.filter(id=test['id']).update(**kwargs)
            step_list.remove({"id": test['id']})
        else:
            kwargs['case'] = case
            models.CaseStep.objects.create(**kwargs)

    #  去掉多余的step
    for content in step_list:
        models.CaseStep.objects.filter(id=content['id']).delete()


def generate_casestep(body, case):
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
            else:
                api = models.API.objects.get(id=test['id'])
                new_body = eval(api.body)
                name = test['body']['name']

                if api.name != name:
                    new_body['name'] = name

                url = test['body']['url']
                method = test['body']['method']

        kwargs = {
            "name": name,
            "body": new_body,
            "url": url,
            "method": method,
            "step": index,
            "case": case
        }

        models.CaseStep.objects.create(**kwargs)


def case_end(pk):
    """
    pk: int case id
    """
    models.CaseStep.objects.filter(case__id=pk).delete()
    models.Case.objects.filter(id=pk).delete()
