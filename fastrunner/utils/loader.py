import io
import json
import types
import yaml
from httprunner import HttpRunner, logger
from fastrunner import models


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



if __name__ == "__main__":
    pass

    # kwargs = {
    #     "failfast": False
    # }
    #
    # runner = HttpRunner(**kwargs)
    #
    # testcase_list = [
    #     # testcase data structure
    #     {
    #         'config': {
    #             'name': 'testset description',
    #             'path': 'docs/data/demo-quickstart-2.yml',
    #             'request': {
    #                 'base_url': '',
    #                 'headers': {'User-Agent': 'python-requests/2.18.4'}
    #             },
    #             'variables': [],
    #             'output': ['token']
    #         },
    #         'api': {},
    #         "teststeps": [
    #             # teststep data structure
    #             {
    #                 'name': '/api/get-token',
    #                 'request': {
    #                     'url': 'http://127.0.0.1:5000/api/get-token',
    #                     'method': 'POST',
    #                     'headers': {'Content-Type': 'application/json', 'app_version': '2.8.6',
    #                                 'device_sn': 'FwgRiO7CNA50DSU', 'os_platform': 'ios', 'user_agent': 'iOS/10.3'},
    #                     'json': {'sign': '958a05393efef0ac7c0fb80a7eac45e24fd40c27'}
    #                 },
    #                 'extract': [
    #                     {'token': 'content.token'}
    #                 ],
    #                 "setup_hooks": [
    #                     "${time_sleep(4)}"
    #                 ],
    #                 'validate': [
    #                     {'eq': ['status_code', 200]},
    #                     {'eq': ['headers.Content-Type', 'application/json']},
    #                     {'eq': ['content.success', True]}
    #                 ]
    #             },
    #             {
    #                 'name': '/api/users/1000',
    #                 'request': {
    #                     'url': 'http://127.0.0.1:5000/api/users/1000',
    #                     'method': 'POST',
    #                     'headers': {'Content-Type': 'application/json', 'device_sn': 'FwgRiO7CNA50DSU',
    #                                 'token': '$token'}, 'json': {'name': 'user1', 'password': '123456'}
    #                 },
    #                 'validate': [
    #                     {'eq': ['status_code', 201]},
    #                     {'eq': ['headers.Content-Type', 'application/json']},
    #                     {'eq': ['content.success', True]},
    #                     {'eq': ['content.msg', 'user created successfully.']}
    #                 ]
    #             }
    #         ]
    #     },
    #
    # ]
    # debugtalk = FileLoader.load_python_module(tests)
    #
    # runner.run(testcase_list, mapping={"debugtalk": debugtalk})
