import io
import json
import types
import yaml
from httprunner import HttpRunner, logger
from fastrunner import models
from fastrunner.utils.parser import Format


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
    def load_python_module(module):
        """ load python module.

        Args:
            module: python module

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

        for name, item in vars(module).items():
            print(name, item)
            if is_function((name, item)):
                debugtalk_module["functions"][name] = item
            elif is_variable((name, item)):
                if isinstance(item, tuple):
                    continue
                debugtalk_module["variables"][name] = item
            else:
                pass

        return debugtalk_module


def parse_tests(testcases, config=None):
    """get test case structure
        testcases: list
        config: none or dict
    """
    testcases = {
        "teststeps": testcases,
    }

    if config:
        testcases["config"] = config

    return testcases


def debug_api(api, pk):
    """debug api
        api :dict
        pk: int
    """
    body = None

    if pk:
        config = models.Config.objects.get(id=pk)
        body = eval(config.body)

    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    testcase_list = [parse_tests(api, config=body)]

    logger.setup_logger('DEBUG')

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
