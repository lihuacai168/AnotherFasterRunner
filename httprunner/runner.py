# encoding: utf-8
import threading

import pydash
import time
from unittest.case import SkipTest

from httprunner import exceptions, logger, response, utils
from httprunner.client import HttpSession
from httprunner.compat import OrderedDict
from httprunner.context import Context


class Runner(object):
    # 每个线程对应Runner类的实例
    instances = {}

    def __init__(self, config_dict=None, http_client_session=None):
        """
        """
        self.http_client_session = http_client_session
        config_dict = config_dict or {}
        self.evaluated_validators = []

        # testcase variables
        config_variables = config_dict.get("variables", {})
        # testcase functions
        config_functions = config_dict.get("functions", {})
        # testcase setup hooks
        testcase_setup_hooks = config_dict.pop("setup_hooks", [])
        # testcase teardown hooks
        self.testcase_teardown_hooks = config_dict.pop("teardown_hooks", [])

        self.context = Context(config_variables, config_functions)
        self.init_test(config_dict, "testcase")

        if testcase_setup_hooks:
            self.do_hook_actions(testcase_setup_hooks)

        Runner.instances[threading.current_thread().name] = self

    def __del__(self):
        if self.testcase_teardown_hooks:
            self.do_hook_actions(self.testcase_teardown_hooks)

    def init_test(self, test_dict, level):
        """ create/update context variables binds

        Args:
            test_dict (dict):
            level (enum): "testcase" or "teststep"
                testcase:
                    {
                        "name": "testcase description",
                        "variables": [],   # optional
                        "request": {
                            "base_url": "http://127.0.0.1:5000",
                            "headers": {
                                "User-Agent": "iOS/2.8.3"
                            }
                        }
                    }
                teststep:
                    {
                        "name": "teststep description",
                        "variables": [],   # optional
                        "request": {
                            "url": "/api/get-token",
                            "method": "POST",
                            "headers": {
                                "Content-Type": "application/json"
                            }
                        },
                        "json": {
                            "sign": "f1219719911caae89ccc301679857ebfda115ca2"
                        }
                    }

        Returns:
            dict: parsed request dict

        """
        test_dict = utils.lower_test_dict_keys(test_dict)

        self.context.init_context_variables(level)
        variables = test_dict.get('variables') \
            or test_dict.get('variable_binds', OrderedDict())
        self.context.update_context_variables(variables, level)

        request_config = test_dict.get('request', {})
        parsed_request = self.context.get_parsed_request(request_config, level)

        base_url = parsed_request.pop("base_url", None)
        self.http_client_session = self.http_client_session or HttpSession(base_url)

        return parsed_request

    def _handle_skip_feature(self, teststep_dict):
        """ handle skip feature for teststep
            - skip: skip current test unconditionally
            - skipIf: skip current test if condition is true
            - skipUnless: skip current test unless condition is true

        Args:
            teststep_dict (dict): teststep info

        Raises:
            SkipTest: skip teststep

        """
        # TODO: move skip to initialize
        skip_reason = None

        if "skip" in teststep_dict:
            skip_reason = teststep_dict["skip"]

        elif "skipIf" in teststep_dict:
            skip_if_condition = teststep_dict["skipIf"]
            if self.context.eval_content(skip_if_condition):
                skip_reason = "{} evaluate to True".format(skip_if_condition)

        elif "skipUnless" in teststep_dict:
            skip_unless_condition = teststep_dict["skipUnless"]
            if not self.context.eval_content(skip_unless_condition):
                skip_reason = "{} evaluate to False".format(skip_unless_condition)

        if skip_reason:
            raise SkipTest(skip_reason)

    def do_hook_actions(self, actions):
        for action in actions:
            logger.log_debug("call hook: {}".format(action))
            # TODO: check hook function if valid
            self.context.eval_content(action)

    def run_test(self, teststep_dict):
        """ run single teststep.

        Args:
            teststep_dict (dict): teststep info
                {
                    "name": "teststep description",
                    "skip": "skip this test unconditionally",
                    "times": 3,
                    "variables": [],        # optional, override
                    "request": {
                        "url": "http://127.0.0.1:5000/api/users/1000",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json",
                            "authorization": "$authorization",
                            "random": "$random"
                        },
                        "body": '{"name": "user", "password": "123456"}'
                    },
                    "extract": [],              # optional
                    "validate": [],             # optional
                    "setup_hooks": [],          # optional
                    "teardown_hooks": []        # optional
                }

        Raises:
            exceptions.ParamsError
            exceptions.ValidationFailure
            exceptions.ExtractFailure

        """
        # check skip
        self._handle_skip_feature(teststep_dict)

        # prepare
        extractors = teststep_dict.get("extract", []) or teststep_dict.get("extractors", [])
        validators = teststep_dict.get("validate", []) or teststep_dict.get("validators", [])
        parsed_request = self.init_test(teststep_dict, level="teststep")
        self.context.update_teststep_variables_mapping("request", parsed_request)

        # setup hooks
        setup_hooks = teststep_dict.get("setup_hooks", [])
        setup_hooks.insert(0, "${setup_hook_prepare_kwargs($request)}")
        setup_hooks_start = time.time()
        self.do_hook_actions(setup_hooks)
        # 计算前置setup_hooks消耗的时间
        setup_hooks_duration = 0
        self.http_client_session.meta_data['request']['setup_hooks_start'] = setup_hooks_start
        if len(setup_hooks) > 1:
            setup_hooks_duration = time.time() - setup_hooks_start
        self.http_client_session.meta_data['request']['setup_hooks_duration'] = setup_hooks_duration

        try:
            url = parsed_request.pop('url')
            method = parsed_request.pop('method')
            group_name = parsed_request.pop("group", None)
        except KeyError:
            raise exceptions.ParamsError("URL or METHOD missed!")

        # TODO: move method validation to json schema
        valid_methods = ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
        if method.upper() not in valid_methods:
            err_msg = u"Invalid HTTP method! => {}\n".format(method)
            err_msg += "Available HTTP methods: {}".format("/".join(valid_methods))
            logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)

        logger.log_info("{method} {url}".format(method=method, url=url))
        logger.log_debug("request kwargs(raw): {kwargs}".format(kwargs=parsed_request))

        user_timeout: str = str(pydash.get(parsed_request, 'headers.timeout'))
        if user_timeout and user_timeout.isdigit():
            parsed_request['timeout'] = int(user_timeout)

        # request
        resp = self.http_client_session.request(
            method,
            url,
            name=group_name,
            **parsed_request
        )
        resp_obj = response.ResponseObject(resp)

        # teardown hooks
        teardown_hooks = teststep_dict.get("teardown_hooks", [])
        # 计算teardown_hooks消耗的时间
        teardown_hooks_duration = 0
        teardown_hooks_start = time.time()
        if teardown_hooks:
            logger.log_info("start to run teardown hooks")
            self.context.update_teststep_variables_mapping("response", resp_obj)
            self.do_hook_actions(teardown_hooks)
            teardown_hooks_duration = time.time() - teardown_hooks_start
        self.http_client_session.meta_data['response']['teardown_hooks_start'] = teardown_hooks_start
        self.http_client_session.meta_data['response']['teardown_hooks_duration'] = teardown_hooks_duration

        # extract
        extracted_variables_mapping = resp_obj.extract_response(extractors)
        self.context.update_testcase_runtime_variables_mapping(extracted_variables_mapping)

        # validate
        try:
            self.evaluated_validators = self.context.validate(validators, resp_obj)
        except (exceptions.ParamsError, exceptions.ValidationFailure, exceptions.ExtractFailure):
            # log request
            err_req_msg = "request: \n"
            err_req_msg += "headers: {}\n".format(parsed_request.pop("headers", {}))
            for k, v in parsed_request.items():
                err_req_msg += "{}: {}\n".format(k, repr(v))
            logger.log_error(err_req_msg)

            # log response
            err_resp_msg = "response: \n"
            err_resp_msg += "status_code: {}\n".format(resp_obj.status_code)
            err_resp_msg += "headers: {}\n".format(resp_obj.headers)
            err_resp_msg += "body: {}\n".format(repr(resp_obj.text))
            logger.log_error(err_resp_msg)

            raise

    def extract_output(self, output_variables_list):
        """ extract output variables
        """
        variables_mapping = self.context.teststep_variables_mapping

        output = {}
        for variable in output_variables_list:
            if variable not in variables_mapping:
                logger.log_warning(
                    "variable '{}' can not be found in variables mapping, failed to output!"\
                        .format(variable)
                )
                continue

            output[variable] = variables_mapping[variable]

        return output


class Hrun(object):
    """
    特殊关键字，提供给驱动函数中使用
    可以在驱动函数中，修改配置变量和用例步骤运行时变量
    """

    @staticmethod
    def get_current_context():
        current_thread = threading.current_thread().name
        if Runner.instances.get(current_thread):
            return Runner.instances[current_thread].context
        return Runner().context

    @staticmethod
    def set_config_var(name, value):
        # 在运行时修改配置变量
        current_context = Hrun.get_current_context()
        current_context.TESTCASE_SHARED_VARIABLES_MAPPING[name] = value

    @staticmethod
    def set_config_header(name, value):
        # 在运行时修改配置中请求头的信息
        # 比如: 用例中需要切换账号，实现同时请求头中token和userId
        current_context = Hrun.get_current_context()
        pydash.set_(current_context.TESTCASE_SHARED_REQUEST_MAPPING, f'headers.{name}', value)

    @staticmethod
    def set_step_var(name, value):
        current_context = Hrun.get_current_context()
        current_context.testcase_runtime_variables_mapping[name] = value
