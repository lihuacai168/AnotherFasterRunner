import copy
import datetime
import functools
import importlib
import io
import json
import os
import shutil
import sys
import tempfile
import types
from threading import Thread

import requests
import yaml
from bs4 import BeautifulSoup
from httprunner import HttpRunner, logger
from requests.cookies import RequestsCookieJar
from requests_toolbelt import MultipartEncoder

from fastrunner import models
from fastrunner.utils.parser import Format

logger.setup_logger('DEBUG')

TEST_NOT_EXISTS = {
    "code": "0102",
    "status": False,
    "msg": "节点下没有接口或者用例集"
}


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    name, item = tup
    return isinstance(item, types.FunctionType)


def is_variable(tup):
    """ Takes (name, object) tuple, returns True if it is a variable.
    """
    name, item = tup
    if callable(item):
        # function or class
        return False

    if isinstance(item, types.ModuleType):
        # imported module
        return False

    if name.startswith("_"):
        # private property
        return False

    return True


class FileLoader(object):

    @staticmethod
    def dump_yaml_file(yaml_file, data):
        """ dump yaml file
        """
        with io.open(yaml_file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    @staticmethod
    def dump_json_file(json_file, data):
        """ dump json file
        """
        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)

    @staticmethod
    def dump_python_file(python_file, data):
        """dump python file
        """
        with io.open(python_file, 'w', encoding='utf-8') as stream:
            stream.write(data)

    @staticmethod
    def dump_binary_file(binary_file, data):
        """dump file
        """
        with io.open(binary_file, 'wb') as stream:
            stream.write(data)

    @staticmethod
    def load_python_module(file_path):
        """ load python module.

        Args:
            file_path: python path

        Returns:
            dict: variables and functions mapping for specified python module

                {
                    "variables": {},
                    "functions": {}
                }

        """
        debugtalk_module = {
            "variables": {},
            "functions": {}
        }

        sys.path.insert(0, file_path)
        module = importlib.import_module("debugtalk")
        # 修复重载bug
        importlib.reload(module)
        sys.path.pop(0)

        for name, item in vars(module).items():
            if is_function((name, item)):
                debugtalk_module["functions"][name] = item
            elif is_variable((name, item)):
                if isinstance(item, tuple):
                    continue
                debugtalk_module["variables"][name] = item
            else:
                pass

        return debugtalk_module


def parse_tests(testcases, debugtalk, name=None, config=None):
    """get test case structure
        testcases: list
        config: none or dict
        debugtalk: dict
    """
    refs = {
        "env": {},
        "def-api": {},
        "def-testcase": {},
        "debugtalk": debugtalk
    }
    testset = {
        "config": {
            "name": testcases[-1]["name"],
            "variables": []
        },
        "teststeps": testcases,
    }

    if config:
        testset["config"] = config

    if name:
        testset["config"]["name"] = name

    global_variables = []

    for variables in models.Variables.objects.all().values("key", "value"):
        if testset["config"].get("variables"):
            for content in testset["config"]["variables"]:
                if variables["key"] not in content.keys():
                    global_variables.append({variables["key"]: variables["value"]})
        else:
            global_variables.append({variables["key"]: variables["value"]})

    if not testset["config"].get("variables"):
        testset["config"]["variables"] = global_variables
    else:
        testset["config"]["variables"].extend(global_variables)

    testset["config"]["refs"] = refs

    # for teststep in testcases:
    #     # handle files
    #     if "files" in teststep["request"].keys():
    #         fields = {}
    #
    #         if "data" in teststep["request"].keys():
    #             fields.update(teststep["request"].pop("data"))
    #
    #         for key, value in teststep["request"].pop("files").items():
    #             file_binary = models.FileBinary.objects.get(name=value).body
    #             # file_path = os.path.join(tempfile.mkdtemp(prefix='File'), value)
    #             # FileLoader.dump_binary_file(file_path, file_binary)
    #             fields[key] = (value, file_binary)
    #
    #         teststep["request"]["data"] = MultipartEncoder(fields)
    #         try:
    #             teststep["request"]["headers"]["Content-Type"] = teststep["request"]["data"].content_type
    #         except KeyError:
    #             teststep["request"].setdefault("headers", {"Content-Type": teststep["request"]["data"].content_type})

    return testset


def load_debugtalk(project):
    """import debugtalk.py in sys.path and reload
        project: int
    """
    # debugtalk.py
    code = models.Debugtalk.objects.get(project__id=project).code

    file_path = os.path.join(tempfile.mkdtemp(prefix='FasterRunner'), "debugtalk.py")
    FileLoader.dump_python_file(file_path, code)
    debugtalk = FileLoader.load_python_module(os.path.dirname(file_path))

    shutil.rmtree(os.path.dirname(file_path))
    return debugtalk


def debug_suite(suite, project, obj, config=None, save=True):
    """debug suite
           suite :list
           pk: int
           project: int
    """
    if len(suite) == 0:
        return TEST_NOT_EXISTS

    debugtalk = load_debugtalk(project)

    test_sets = []

    for index in range(len(suite)):
        # copy.deepcopy 修复引用bug
        testcases = copy.deepcopy(parse_tests(suite[index], debugtalk, name=obj[index]['name'], config=config))
        test_sets.append(testcases)

    kwargs = {
        "failfast": False
    }
    runner = HttpRunner(**kwargs)
    runner.run(test_sets)
    summary = parse_summary(runner.summary)

    if save:
        save_summary("", summary, project, type=1)

    return summary


def debug_api(api, project, name=None, config=None, save=True):
    """debug api
        api :dict or list
        project: int
    """
    if len(api) == 0:
        return TEST_NOT_EXISTS

    # testcases
    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    testcase_list = [parse_tests(api, load_debugtalk(project), name=name, config=config)]

    kwargs = {
        "failfast": False
    }

    runner = HttpRunner(**kwargs)
    runner.run(testcase_list)

    summary = parse_summary(runner.summary)

    if save:
        save_summary("", summary, project, type=1)

    return summary


def load_test(test, project=None):
    """
    format testcase
    """

    try:
        format_http = Format(test['newBody'])
        format_http.parse()
        testcase = format_http.testcase

    except KeyError:
        if 'case' in test.keys():
            if test["body"]["method"] == "config":
                case_step = models.Config.objects.get(name=test["body"]["name"], project=project)
            else:
                case_step = models.CaseStep.objects.get(id=test['id'])
        else:
            if test["body"]["method"] == "config":
                case_step = models.Config.objects.get(name=test["body"]["name"], project=project)
            else:
                case_step = models.API.objects.get(id=test['id'])

        testcase = eval(case_step.body)
        name = test['body']['name']

        if case_step.name != name:
            testcase['name'] = name

    return testcase


def back_async(func):
    """异步执行装饰器
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


def parse_summary(summary):
    """序列化summary
    """
    for detail in summary["details"]:

        for record in detail["records"]:

            for key, value in record["meta_data"]["request"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["request"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["request"][key] = requests.utils.dict_from_cookiejar(value)

            for key, value in record["meta_data"]["response"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["response"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["response"][key] = requests.utils.dict_from_cookiejar(value)

            if "text/html" in record["meta_data"]["response"]["content_type"]:
                record["meta_data"]["response"]["content"] = \
                    BeautifulSoup(record["meta_data"]["response"]["content"], features="html.parser").prettify()

    return summary


def save_summary(name, summary, project, type=2):
    """保存报告信息
    """
    if "status" in summary.keys():
        return
    if name is "":
        name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    models.Report.objects.create(**{
        "project": models.Project.objects.get(id=project),
        "name": name,
        "type": type,
        "summary": json.dumps(summary, ensure_ascii=False),
    })


@back_async
def async_debug_api(api, project, name):
    """异步执行api
    """
    summary = debug_api(api, project, save=False)
    save_summary(name, summary, project)


@back_async
def async_debug_suite(suite, project, report, obj, config=None):
    """异步执行suite
    """
    summary = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(report, summary, project)
