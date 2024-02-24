import concurrent
import copy
import datetime
import functools
import importlib
import io
import json
import logging
import os
import shutil
import sys
import tempfile
import time
import types
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import requests
import yaml
from bs4 import BeautifulSoup

# from loguru import logger
from requests.cookies import RequestsCookieJar

from FasterRunner.settings.base import BASE_DIR
from fastrunner import models
from fastrunner.utils.parser import Format
from fastrunner.views.report import ConvertRequest
from httprunner import parser
from httprunner.api import HttpRunner
from httprunner.exceptions import FunctionNotFound, VariableNotFound

logger = logging.getLogger(__name__)


TEST_NOT_EXISTS = {"code": "0102", "status": False, "msg": "节点下没有接口或者用例集"}


def is_function(tup):
    """Takes (name, object) tuple, returns True if it is a function."""
    name, item = tup
    return isinstance(item, types.FunctionType)


def is_variable(tup):
    """Takes (name, object) tuple, returns True if it is a variable."""
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
        """dump yaml file"""
        with io.open(yaml_file, "w", encoding="utf-8") as stream:
            yaml.dump(
                data,
                stream,
                indent=4,
                default_flow_style=False,
                encoding="utf-8",
                allow_unicode=True,
            )

    @staticmethod
    def dump_json_file(json_file, data):
        """dump json file"""
        with io.open(json_file, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=4, separators=(",", ": "), ensure_ascii=False)

    @staticmethod
    def dump_python_file(python_file, data):
        """dump python file"""
        with io.open(python_file, "w", encoding="utf-8") as stream:
            stream.write(data)

    @staticmethod
    def dump_binary_file(binary_file, data):
        """dump file"""
        with io.open(binary_file, "wb") as stream:
            stream.write(data)

    @staticmethod
    def load_python_module(file_path):
        """load python module.

        Args:
            file_path: python path

        Returns:
            dict: variables and functions mapping for specified python module

                {
                    "variables": {},
                    "functions": {}
                }

        """
        debugtalk_module = {"variables": {}, "functions": {}}
        debugtalk_module_name = "debugtalk"
        # 修复切换项目后，debugtalk有缓存
        if sys.modules.get(debugtalk_module_name):
            del sys.modules[debugtalk_module_name]
        sys.path.insert(0, file_path)
        module = importlib.import_module(debugtalk_module_name)
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


def parse_validate_and_extract(list_of_dict: list, variables_mapping: dict, functions_mapping, api_variables: list):
    """
    Args:
        list_of_dict (list)
        variables_mapping (dict): variables mapping.
        functions_mapping (dict): functions mapping.
        api_variables: (list)
    Returns:
        引用传参，直接修改dict的内容，不需要返回
    """

    # 获取api中所有变量的key
    api_variables_key = []
    for variable in api_variables:
        api_variables_key.extend(list(variable.keys()))

    for index, d in enumerate(list_of_dict):
        is_need_parse = True
        # extract: d是{'k':'v'}, v类型是str
        # validate: d是{'equals': ['v1', 'v2']}， v类型是list
        v = list(d.values())[0]
        try:
            # validate,extract 的值包含了api variable的key中，不需要替换
            for key in api_variables_key:
                if isinstance(v, str):
                    if key in v:
                        is_need_parse = False
                elif isinstance(v, list):
                    # v[1]需要统一转换成str类型，否则v[1]是int类型就会报错
                    if key in str(v[1]):
                        is_need_parse = False

            if is_need_parse is True:
                d = parser.parse_data(
                    d,
                    variables_mapping=variables_mapping,
                    functions_mapping=functions_mapping,
                )
                for k, v in d.items():
                    v = parser.parse_string_functions(
                        v,
                        variables_mapping=variables_mapping,
                        functions_mapping=functions_mapping,
                    )
                    d[k] = v
                list_of_dict[index] = d
        except (FunctionNotFound, VariableNotFound):
            continue


def parse_tests(testcases, debugtalk, name=None, config=None, project=None):
    """get test case structure
    testcases: list
    config: none or dict
    debugtalk: dict
    """
    refs = {"env": {}, "def-api": {}, "def-testcase": {}, "debugtalk": debugtalk}

    testset = {
        "config": {"name": testcases[-1]["name"], "variables": []},
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

    # 配置中的变量和全局变量合并
    variables_mapping = {}
    if config:
        for variables in config["variables"]:
            variables_mapping.update(variables)

    # 驱动代码中的所有函数
    functions_mapping = debugtalk.get("functions", {})

    # 替换extract,validate中的变量和函数，只对value有效，key无效
    for testcase in testcases:
        extract: list = testcase.get("extract", [])
        validate: list = testcase.get("validate", [])
        api_variables: list = testcase.get("variables", [])
        parse_validate_and_extract(extract, variables_mapping, functions_mapping, api_variables)
        parse_validate_and_extract(validate, variables_mapping, functions_mapping, api_variables)

    return testset


def load_debugtalk(project):
    """import debugtalk.py in sys.path and reload
    project: int
    """
    # debugtalk.py
    code = models.Debugtalk.objects.get(project__id=project).code

    # file_path = os.path.join(tempfile.mkdtemp(prefix='FasterRunner'), "debugtalk.py")
    tempfile_path = tempfile.mkdtemp(prefix="FasterRunner", dir=os.path.join(BASE_DIR, "tempWorkDir"))
    file_path = os.path.join(tempfile_path, "debugtalk.py")
    os.chdir(tempfile_path)
    try:
        FileLoader.dump_python_file(file_path, code)
        debugtalk = FileLoader.load_python_module(os.path.dirname(file_path))
        return debugtalk, file_path

    except Exception:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(file_path))


def merge_parallel_result(results: list, duration):
    """合并并行的结果，保持和串行运行结果一样"""
    base_result: dict = results.pop()
    for result in results:
        base_result["success"] = result["success"] and base_result["success"]
        for k, v in base_result["stat"].items():
            base_result["stat"][k] = v + result["stat"][k]

        for k, v in base_result["time"].items():
            if k == "start_at":
                base_result["time"][k] = min(v, result["time"][k])
            else:
                base_result["time"][k] = v + result["time"][k]
        base_result["details"].extend(result["details"])
    base_result["time"]["duration"] = duration

    # 删除多余的key
    keys = list(base_result.keys())
    for k in keys:
        if k not in ("success", "stat", "time", "platform", "details"):
            base_result.pop(k)
    return base_result


def debug_suite_parallel(test_sets: list):
    """并行运行用例"""

    def run_test(test_set: dict):
        kwargs = {"failfast": False}
        runner = HttpRunner(**kwargs)
        runner.run([test_set])
        return parse_summary(runner.summary)

    start = time.time()
    # 限制最多10个线程
    workers = min(len(test_sets), 10)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_test, t): t for t in test_sets}
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    duration = time.time() - start
    return merge_parallel_result(results, duration)


def debug_suite(
    suite,
    project,
    obj,
    config=None,
    save=True,
    user="",
    report_type=1,
    report_name="",
    allow_parallel=False,
):
    """
    suite : list[list[dict]], 用例列表
    project: int, 项目id
    obj: dict {'case_id': int 'case_name': str}, 用例的名称和id
    config: list[dict], 每个用例运行的配置
    report_type: int, 默认类型是调试
    """
    if len(suite) == 0:
        return TEST_NOT_EXISTS

    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]
    os.chdir(os.path.dirname(debugtalk_path))
    test_sets = []
    # 先记录配置的名称，parse_tests会改变config
    config_name_list = [d["name"] for d in config]
    try:
        for index in range(len(suite)):
            # copy.deepcopy 修复引用bug
            # testcases = copy.deepcopy(parse_tests(suite[index], debugtalk, name=obj[index]['name'], config=config[index]))
            testcases = copy.deepcopy(
                parse_tests(
                    suite[index],
                    debugtalk_content,
                    name=obj[index]["name"],
                    config=config[index],
                    project=project,
                )
            )
            test_sets.append(testcases)

        if allow_parallel:
            summary = debug_suite_parallel(test_sets)
        else:
            kwargs = {"failfast": False}
            runner = HttpRunner(**kwargs)
            runner.run(test_sets)
            summary = parse_summary(runner.summary)
        # 统计用例级别的数据
        details: list = summary["details"]
        failure_case_config_mapping_list = []
        for index, details in enumerate(details):
            if details["success"] is False:
                # 用例失败时,记录用例执行的配置
                failure_case_config = {"config_name": config_name_list[index]}
                failure_case_config.update(obj[index])
                failure_case_config_mapping_list.append(failure_case_config)
        case_count = len(test_sets)
        case_fail_rate = "{:.2%}".format(len(failure_case_config_mapping_list) / case_count)
        summary["stat"].update(
            {
                "failure_case_config_mapping_list": failure_case_config_mapping_list,
                "case_count": case_count,
                "case_fail_rate": case_fail_rate,
                "project": project,
            }
        )
        report_id = 0
        if save:
            report_id = save_summary(
                report_name or f"批量运行{len(test_sets)}条用例",
                summary,
                project,
                type=report_type,
                user=user,
            )
        # 复制一份response的json
        for details in summary.get("details", []):
            for record in details.get("records", []):
                json_data = record["meta_data"]["response"].pop("json", {})
                if json_data:
                    record["meta_data"]["response"]["jsonCopy"] = json_data
        return summary, report_id

    except Exception as e:
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))


def debug_api(api, project, name=None, config=None, save=True, user=""):
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
    if config and config.get("parameters"):
        api_params = []
        for item in api:
            params = item["request"].get("params") or item["request"].get("json")
            for v in params.values():
                if type(v) == list:
                    api_params.extend(v)
                else:
                    api_params.append(v)
        parameters = []
        for index, dic in enumerate(config["parameters"]):
            for key in dic.keys():
                # key可能是key-key1这种模式,所以需要分割
                for i in key.split("-"):
                    if "$" + i in api_params:
                        parameters.append(dic)
        config["parameters"] = parameters

    debugtalk = load_debugtalk(project)
    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]
    os.chdir(os.path.dirname(debugtalk_path))
    try:
        # testcase_list = [parse_tests(api, load_debugtalk(project), name=name, config=config)]
        testcase_list = [parse_tests(api, debugtalk_content, name=name, config=config, project=project)]

        kwargs = {"failfast": False}

        runner = HttpRunner(**kwargs)
        runner.run(testcase_list)

        summary = parse_summary(runner.summary)

        if save:
            save_summary(name, summary, project, type=1, user=user)

        # 复制一份response的json
        for details in summary.get("details", []):
            for record in details.get("records", []):
                json_data = record["meta_data"]["response"].pop("json", {})
                if json_data:
                    record["meta_data"]["response"]["jsonCopy"] = json_data
        ConvertRequest.generate_curl(summary["details"], convert_type=("curl", "boomer"))
        return summary
    except Exception as e:
        logger.error(f"debug_api error: {e}")
        raise SyntaxError(str(e))
    finally:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))


def load_test(test, project=None):
    """
    format testcase
    """

    try:
        format_http = Format(test["newBody"])
        format_http.parse()
        testcase = format_http.testcase

    except KeyError:
        if "case" in test.keys():
            if test["body"]["method"] == "config":
                case_step = models.Config.objects.get(name=test["body"]["name"], project=project)
            else:
                case_step = models.CaseStep.objects.get(id=test["id"])
        else:
            if test["body"]["method"] == "config":
                case_step = models.Config.objects.get(name=test["body"]["name"], project=project)
            else:
                case_step = models.API.objects.get(id=test["id"])

        testcase = eval(case_step.body)
        name = test["body"]["name"]

        if case_step.name != name:
            testcase["name"] = name

    return testcase


def back_async(func):
    """异步执行装饰器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


def parse_summary(summary):
    """序列化summary"""
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
                record["meta_data"]["response"]["content"] = BeautifulSoup(
                    record["meta_data"]["response"]["content"], features="html.parser"
                ).prettify()

    return summary


def save_summary(name, summary, project, type=2, user="", ci_metadata={}):
    """保存报告信息"""
    if "status" in summary.keys():
        return
    if name == "" or name is None:
        name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 需要先复制一份,不然会把影响到debug_api返回给前端的报告
    summary = copy.copy(summary)
    summary_detail = summary.pop("details")
    report = models.Report.objects.create(
        **{
            "project": models.Project.objects.get(id=project),
            "name": name,
            "type": type,
            "status": summary["success"],
            "summary": json.dumps(summary, ensure_ascii=False),
            "creator": user,
            "ci_metadata": ci_metadata,
            "ci_project_id": ci_metadata.get("ci_project_id"),
            "ci_job_id": ci_metadata.get("ci_job_id", None),
        }
    )

    models.ReportDetail.objects.create(summary_detail=summary_detail, report=report)
    return report.id


@back_async
def async_debug_api(api, project, name, config=None):
    """异步执行api"""
    summary = debug_api(api, project, save=False, config=config)
    save_summary(name, summary, project)


@back_async
def async_debug_suite(suite, project, report, obj, config=None):
    """异步执行suite"""
    summary, _ = debug_suite(suite, project, obj, config=config, save=False)
    save_summary(report, summary, project)
