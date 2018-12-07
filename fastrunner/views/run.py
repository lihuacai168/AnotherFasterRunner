from rest_framework.decorators import api_view
from fastrunner.utils import loader
from rest_framework.response import Response
from fastrunner.utils.parser import Format
from fastrunner import models

"""运行方式
"""


@api_view(['POST'])
def run_api(request):
    """ run api by body and config
    """
    config = request.data.pop("config")
    api = Format(request.data)
    api.parse()

    summary = loader.debug_api(api.testcase, config, api.project)

    return Response(summary)


@api_view(['GET'])
def run_api_pk(request, **kwargs):
    """run api by pk and config
    """
    api = models.API.objects.get(id=kwargs['pk'])
    testcase = eval(api.body)

    summary = loader.debug_api(testcase, request.query_params["config"], api.project.id)

    return Response(summary)


@api_view(['POST'])
def run_api_tree(request):
    """run api by tree
    {
        project: int
        relation: list
        config: int
        name: str
        async: bool
    }
    """
    # order by id default
    project = request.data['project']
    relation = request.data["relation"]
    async = request.data["async"]
    name = request.data["name"]
    config = request.data["config"]

    testcase = []
    for relation_id in relation:
        api = models.API.objects.filter(project__id=project, relation=relation_id).order_by('id').values('body')
        for content in api:
            testcase.append(eval(content['body']))
    if async:
        loader.async_debug_api(testcase, config, project, name)
        summary = loader.TEST_NOT_EXISTS
        summary["msg"] = "接口运行中，请稍后查看报告"
    else:
        summary = loader.debug_api(testcase, config, project)

    return Response(summary)


@api_view(["POST"])
def run_testsuite(request):
    """debug testsuite
    {
        name: str,
        config: int
        body: dict
    }
    """
    body = request.data["body"]

    testcase_list = []

    for test in body:
        testcase_list.append(loader.load_test(test))

    summary = loader.debug_api(testcase_list, request.data['config'], request.data["project"])

    return Response(summary)


@api_view(["POST"])
def run_test(request):
    """debug single test
    {
        config: int
        body: dict
    }
    """

    body = request.data["body"]
    summary = loader.debug_api(loader.load_test(body), request.data["config"], request.data["project"])
    return Response(summary)


@api_view(["GET"])
def run_testsuite_pk(request, **kwargs):
    """run testsuite by pk
        pk: int
        config: int
    """
    pk = kwargs["pk"]

    test_list = models.CaseStep.objects. \
        filter(case__id=pk).order_by("step").values("body")

    testcase_list = []

    for content in test_list:
        testcase_list.append(eval(content["body"]))

    summary = loader.debug_api(testcase_list, request.query_params["config"], request.query_params["project"])

    return Response(summary)


@api_view(['POST'])
def run_suite_tree(request):
    """run suite by tree
    {
        project: int
        relation: list
        config: int
        name: str
        async: bool
    }
    """
    # order by id default
    project = request.data['project']
    relation = request.data["relation"]
    async = request.data["async"]
    name = request.data["name"]
    config = request.data["config"]

    testcase = []
    for relation_id in relation:
        suite = models.Case.objects.filter(project__id=project, relation=relation_id).order_by('id').values('id')

        for content in suite:
            test_list = models.CaseStep.objects. \
                filter(case__id=content["id"]).order_by("step").values("body")
            # [{scripts}, {scripts}]
            testcase_list = []

            for content in test_list:
                testcase_list.append(eval(content["body"]))
            # [[{scripts}, {scripts}], [{scripts}, {scripts}]]
            testcase.append(testcase_list)

    if async:
        loader.async_debug_suite(testcase, config, project, name)
        summary = loader.TEST_NOT_EXISTS
        summary["msg"] = "用例运行中，请稍后查看报告"
    else:
        summary = loader.debug_suite(testcase, config, project)

    return Response(summary)
