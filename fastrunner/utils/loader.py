import importlib
import io
import json
import os
import shutil
import sys
import tempfile
import types

import yaml
from httprunner import HttpRunner, logger
from requests_toolbelt import MultipartEncoder

from fastrunner import models
from fastrunner.utils.parser import Format

logger.setup_logger('DEBUG')

TEST_NOT_EXISTS = {
    "code": "0102",
    "status": False,
    "msg": "没有接口或者用例集"
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


def parse_tests(testcases, debugtalk, config=None):
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
            "name": testcases[-1]["name"]
        },
        "teststeps": testcases,
    }

    if config:
        testset["config"] = config

    testset["config"]["refs"] = refs

    for teststep in testcases:
        # handle files
        if "files" in teststep["request"].keys():
            fields = {}

            if "data" in teststep["request"].keys():
                fields.update(teststep["request"].pop("data"))

            for key, value in teststep["request"].pop("files").items():
                file_binary = models.FileBinary.objects.get(name=value).body
                # file_path = os.path.join(tempfile.mkdtemp(prefix='File'), value)
                # FileLoader.dump_binary_file(file_path, file_binary)
                fields[key] = (value, file_binary)

            teststep["request"]["data"] = MultipartEncoder(fields)
            try:
                teststep["request"]["headers"]["Content-Type"] = teststep["request"]["data"].content_type
            except KeyError:
                teststep["request"].setdefault("headers", {"Content-Type": teststep["request"]["data"].content_type})

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


def debug_suite(suite, pk, project):
    """debug suite
           suite :list
           pk: int
           project: int
    """
    if len(suite) == 0:
        return TEST_NOT_EXISTS
    body = None
    # config
    if pk:
        config = models.Config.objects.get(id=pk)
        body = eval(config.body)

    debugtalk = load_debugtalk(project)

    testsuite = []
    for testcase in suite:
        testsuite.append(parse_tests(testcase, debugtalk, config=body))

    kwargs = {
        "failfast": False
    }

    runner = HttpRunner(**kwargs)
    runner.run(testsuite)
    return runner.summary


def debug_api(api, pk, project):
    """debug api
        api :dict or list
        pk: int
        project: int
    """
    if len(api) == 0:
        return TEST_NOT_EXISTS

    body = None
    # config
    if pk:
        config = models.Config.objects.get(id=pk)
        body = eval(config.body)

    # testcases
    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    testcase_list = [parse_tests(api, load_debugtalk(project), config=body)]

    kwargs = {
        "failfast": False
    }

    runner = HttpRunner(**kwargs)
    runner.run(testcase_list)
    return runner.summary


def load_test(test):
    """
    format testcase
    """

    try:
        format_http = Format(test['newBody'])
        format_http.parse()
        testcase = format_http.testcase

    except KeyError:
        if 'case' in test.keys():
            case_step = models.CaseStep.objects.get(id=test['id'])
        else:
            case_step = models.API.objects.get(id=test['id'])

        testcase = eval(case_step.body)
        name = test['body']['name']

        if case_step.name != name:
            testcase['name'] = name

    return testcase
