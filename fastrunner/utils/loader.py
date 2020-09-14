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
from FasterRunner.settings.base import BASE_DIR

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
            yaml.dump(
                data,
                stream,
                indent=4,
                default_flow_style=False,
                encoding='utf-8',
                allow_unicode=True)

    @staticmethod
    def dump_json_file(json_file, data):
        """ dump json file
        """
        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(
                data, stream, indent=4, separators=(
                    ',', ': '), ensure_ascii=False)

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


def parse_tests(testcases, debugtalk, name=None, config=None, project=None):
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

    # 获取当前项目的全局变量
    global_variables = models.Variables.objects.filter(project=project).all().values("key", "value")
    all_config_variables_keys = set().union(*(d.keys() for d in testset["config"].setdefault("variables", [])))
    global_variables_list_of_dict = []
    for item in global_variables:
        if item["key"] not in all_config_variables_keys:
            global_variables_list_of_dict.append({item["key"]: item["value"]})

    # 有variables就直接extend,没有就加一个[],再extend
    # 配置的variables和全局变量重叠,优先使用配置中的variables
    testset["config"].setdefault("variables", []).extend(global_variables_list_of_dict)
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

    # file_path = os.path.join(tempfile.mkdtemp(prefix='FasterRunner'), "debugtalk.py")
    tempfile_path = tempfile.mkdtemp(
        prefix='FasterRunner', dir=os.path.join(
            BASE_DIR, 'tempWorkDir'))
    file_path = os.path.join(tempfile_path, 'debugtalk.py')
    os.chdir(tempfile_path)
    try:
        FileLoader.dump_python_file(file_path, code)
        debugtalk = FileLoader.load_python_module(os.path.dirname(file_path))
        return debugtalk, file_path

    except Exception as e:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(file_path))


def debug_suite(suite, project, obj, config=None, save=True):
    """debug suite
           suite :list
           pk: int
           project: int
    """
    if len(suite) == 0:
        return TEST_NOT_EXISTS

    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]
    os.chdir(os.path.dirname(debugtalk_path))
    test_sets = []
    try:
        for index in range(len(suite)):
            # copy.deepcopy 修复引用bug
            # testcases = copy.deepcopy(parse_tests(suite[index], debugtalk, name=obj[index]['name'], config=config[index]))
            testcases = copy.deepcopy(
                parse_tests(
                    suite[index],
                    debugtalk_content,
                    name=obj[index]['name'],
                    config=config[index],
                    project=project
                ))
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

    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))


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

    # 参数化过滤,只加载api中调用到的参数
    if config and config.get('parameters'):
        api_params = []
        for item in api:
            params = item['request'].get('params') or item['request'].get('json')
            for v in params.values():
                if type(v) == list:
                    api_params.extend(v)
                else:
                    api_params.append(v)
        parameters = []
        for index, dic in enumerate(config['parameters']):
            for key in dic.keys():
                # key可能是key-key1这种模式,所以需要分割
                for i in key.split('-'):
                    if '$' + i in api_params:
                        parameters.append(dic)
        config['parameters'] = parameters

    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]
    os.chdir(os.path.dirname(debugtalk_path))
    try:
        # testcase_list = [parse_tests(api, load_debugtalk(project), name=name, config=config)]
        testcase_list = [
            parse_tests(
                api,
                debugtalk_content,
                name=name,
                config=config,
                project=project)]

        kwargs = {
            "failfast": False
        }

        runner = HttpRunner(**kwargs)
        runner.run(testcase_list)

        summary = parse_summary(runner.summary)

        if save:
            save_summary("", summary, project, type=1)
        return summary
    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))


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
                case_step = models.Config.objects.get(
                    name=test["body"]["name"], project=project)
            else:
                case_step = models.CaseStep.objects.get(id=test['id'])
        else:
            if test["body"]["method"] == "config":
                case_step = models.Config.objects.get(
                    name=test["body"]["name"], project=project)
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
                    record["meta_data"]["request"][key] = requests.utils.dict_from_cookiejar(
                        value)

            for key, value in record["meta_data"]["response"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["response"][key] = value.decode(
                        "utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["response"][key] = requests.utils.dict_from_cookiejar(
                        value)

            if "text/html" in record["meta_data"]["response"]["content_type"]:
                record["meta_data"]["response"]["content"] = BeautifulSoup(
                    record["meta_data"]["response"]["content"], features="html.parser").prettify()

    return summary


def save_summary(name, summary, project, type=2):
    """保存报告信息
    """
    if "status" in summary.keys():
        return
    if name == "":
        name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 　删除用不到的属性
    summary['details'][0].pop('in_out')
    # 需要先复制一份,不然会把影响到debug_api返回给前端的报告
    summary = copy.copy(summary)
    summary_detail = summary.pop('details')
    report = models.Report.objects.create(**{
        "project": models.Project.objects.get(id=project),
        "name": name,
        "type": type,
        "status": summary['success'],
        "summary": json.dumps(summary, ensure_ascii=False),
    })

    models.ReportDetail.objects.create(summary_detail=summary_detail, report=report)


@back_async
def async_debug_api(api, project, name, config=None):
    """异步执行api
    """
    summary = debug_api(api, project, save=False, config=config)
    save_summary(name, summary, project)


@back_async
def async_debug_suite(suite, project, report, obj, config=None):
    """异步执行suite
    """
    summary = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(report, summary, project)
