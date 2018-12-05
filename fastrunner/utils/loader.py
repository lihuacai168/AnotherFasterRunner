import enum
import importlib
import io
import json
import os
import shutil
import socket
import subprocess
import simplejson
import requests
from requests.cookies import RequestsCookieJar
import signal
import sys
from django.conf import settings
import tempfile, base64
import types

import yaml
from httprunner import HttpRunner, logger
from requests_toolbelt import MultipartEncoder

from fastrunner import models
from fastrunner.utils.parser import Format

logger.setup_logger('INFO')


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


def load_httprunner_tests(api, pk, project):
    """debug api
        api :dict
        pk: int
        project: int
    """
    body = None
    # config
    if pk:
        config = models.Config.objects.get(id=pk)
        body = eval(config.body)

    # debugtalk.py
    code = models.Debugtalk.objects.get(project__id=project).code
    temp_path = tempfile.mkdtemp(prefix='debugtalk_')
    file_path = os.path.join(temp_path, '%s.py' % "debugtalk")
    FileLoader.dump_python_file(file_path, code)
    debugtalk = FileLoader.load_python_module(temp_path)
    shutil.rmtree(temp_path)

    # testcases
    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    testcase_list = [parse_tests(api, debugtalk, config=body)]
    return testcase_list


class Run_type(enum.Enum):
    API = 1
    TEST_SET = 2
    SCHEDULE = 3
    CI = 4


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def encode_complex(obj):
    if isinstance(obj, RequestsCookieJar):
        return requests.utils.dict_from_cookiejar(obj)


def debug_api(api, pk, project, ref=None, refId=None, name='', relation_id=None):
    """debug api
        api :dict
        pk: int
        project: int
    """
    body = None
    config = None
    if pk:
        config = models.Config.objects.get(id=pk)
        body = eval(config.body)

    # debugtalk.py
    code = models.Debugtalk.objects.get(project__id=project).code
    temp_path = tempfile.mkdtemp(prefix='debugtalk_')
    file_path = os.path.join(temp_path, '%s.py' % "debugtalk")
    FileLoader.dump_python_file(file_path, code)
    debugtalk = FileLoader.load_python_module(temp_path)
    shutil.rmtree(temp_path)

    # testcases
    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    testcase_list = [parse_tests(api, debugtalk, config=body)]

    kwargs = {
        "failfast": False
    }

    runner = HttpRunner(**kwargs)
    runner.run(testcase_list)
    summary = runner.summary
    """
    API = 1
    TEST_SET = 2
    SCHEDULE = 3
    """
    if ref is not None and refId is not None:
        if bool(summary['success']):
            status = "success"
        else:
            status = "failure"
        if ref == Run_type.API or ref == Run_type.TEST_SET:
            relationId = models.ReportRelation.objects.create(
                name=name,
                ref=ref.value,
                project=project,
                status=status
            )
            report = models.Report.objects.create(
                content=simplejson.dumps(summary, encoding="UTF-8", default=encode_complex),
                refId=refId,
                reportRelation=relationId
            )
        if ref == Run_type.SCHEDULE or ref == Run_type.CI:
            report = models.Report.objects.create(
                content=simplejson.dumps(summary, encoding="UTF-8", default=encode_complex),
                refId=refId,
                reportRelation=relation_id
            )
            url = settings.SERVICE_URL + '/api/expose/ScheduleReport/' + str(report.id)
            content = '''
----------------------------------

- 步骤名称：{0}
- 步骤结果：{1}
- 执行环境名称：{2}
- 执行环境地址：{3}
- 结果报告地址：{4}

            '''
            content = content.format(name, status, config.name, config.base_url, url)
            summary["report_content"] = content
    return summary


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


def IsOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        print('%d is open' % port)
        return True
    except:
        print('%d is down' % port)
        return False


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def gen_locust(suite_id, config_id, project, progress):
    """ generate locustfile from template.
    """
    if models.LocustDetail.objects.filter(suite_id=suite_id):
        return False, models.LocustDetail.objects.get(suite_id).port, "已存在该压测环境"
    if models.LocustDetail.objects.count() >= 20:
        return False, -1, "当前已有二十个压测环境！，请稍后再尝试创建压测环境"
    test_list = models.CaseStep.objects. \
        filter(case__id=suite_id).order_by("step").values("body")
    name = models.Case.objects.get(id=suite_id).name
    testcase_list = []

    for content in test_list:
        testcase_list.append(eval(content["body"]))
    path = tempfile.mktemp(suffix=".py", prefix="locustsfile")
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "templates",
        "locust_template"
    )
    if config_id == '':
        return False, -1, "请先选择测试环境"
    config = models.Config.objects.get(id=config_id)
    testcases = load_httprunner_tests(testcase_list, config_id, project)
    with io.open(template_path, encoding='utf-8') as template:
        with io.open(path, 'w', encoding='utf-8') as locustfile:
            template_content = template.read()
            template_content = template_content.replace("$HOST", config.base_url)
            template_content = template_content.replace("$TESTCASES", str(testcases))
            locustfile.write(template_content)
        # return path
    port = get_open_port()
    port1 = get_open_port()
    tasks = []
    task = subprocess.Popen(["locust", "-f", path, "--master", "--master-bind-port", str(port), "-P", str(port1)])
    # task = subprocess.Popen("locust -f {0} --master --master-bind-port {1} -P {2}".format(path, port, port1),
    #                         shell=True)
    tasks.append(task.pid)
    for i in range(0, progress):
        subtask = subprocess.Popen(["locust", "-f", path, "--slave", "--master-port", str(port)])
        # subtask = subprocess.Popen("locust -f {0} --slave --master-port {1}".format(path, port), shell=True)
        tasks.append(subtask.pid)
    models.LocustDetail.objects.create(
        suite_id=suite_id,
        suite_name=name,
        config_id=config_id,
        config_name=config.name,
        config_url=config.base_url,
        port=port1,
        project=project,
        task=str(tasks)
    )
    return True, port1, "创建压测环境成功"


def get_locusts(project_id):
    result = []
    for locust in models.LocustDetail.objects.filter(project=project_id).all():
        if int(locust.project) == project_id:
            result.append({
                "suite_id": locust.suite_id,
                "suite_name": locust.suite_name,
                "config_id": locust.config_id,
                "config_name": locust.config_name,
                "config_url": locust.config_url,
                "port": locust.port,
                "project": project_id
            })
    return result


def kill(pid):
    try:
        if os.name == 'nt':
            os.popen('taskkill.exe /pid:' + str(pid))
        else:
            os.kill(pid, signal.SIGKILL)
        print("已经杀死pid为%s的进程" % (pid))
    except Exception as ee:
        print("没有此进程！")


def kill_task(suite_id):
    locust = models.LocustDetail.objects.get(suite_id=suite_id)
    if locust:
        tasks = eval(locust.task)
        try:
            for task in tasks:
                kill(task)
            locust.delete()
            return True, "删除成功"
        except Exception:
            return False, "压测环境关闭失败 请联系管理员"
    else:
        return False, "当前用例集不存在压测环境!"
