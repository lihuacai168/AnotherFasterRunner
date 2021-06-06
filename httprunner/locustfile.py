# coding: utf-8
import json
import logging
import os
import random
import sys
from functools import lru_cache
from pathlib import Path

import gevent
from locust import HttpLocust, TaskSet, task
from httprunner.exceptions import MyBaseError, MyBaseFailure
from httprunner.task import init_test_suites
from httprunner.loader import load_dot_env_file


sys.path.insert(0, os.path.dirname(__file__))
logging.getLogger().setLevel(logging.CRITICAL)
logging.getLogger('locust.main').setLevel(logging.INFO)
logging.getLogger('locust.runners').setLevel(logging.INFO)


def P(relpath):
    abspath = Path(__file__).parent / relpath
    return abspath.resolve()


@lru_cache(maxsize=None)
def load_tests():
    try:
        with open(P('testcase.json'), 'r') as tj:
            items = json.load(tj)
    except FileNotFoundError:
        return {}, []
    try:
        load_dot_env_file(P('.env'))
    except FileNotFoundError:
        pass
    config_obj = {}
    test_objs = []
    for item in items:
        if 'config' in item:
            config_obj = item
        elif 'test' in item:
            test_objs.append(item)
    tests = []
    for idx, test_obj in enumerate(test_objs):
        name = f'{idx}.json'
        with open(P(name), 'w') as fp:
            json.dump([config_obj, test_obj], fp)
        for _ in range(test_obj['test']['weight']):
            tests.append(name)
    config = config_obj['config']
    return config, tests


@lru_cache(maxsize=None)
def get_work(path, client):
    suite = init_test_suites(path, None, client)
    return suite


class WebSiteTasks(TaskSet):
    """all in one
    """
    def on_start(self):
        self.variables = {}
        for variable in self.locust.hrun_config.get('variables', []):
            if 'setup_locust' in variable:
                setup_func_name = variable['setup_locust']
                try:
                    import debugtalk
                    setup_func = getattr(debugtalk, setup_func_name)
                except (AttributeError, ImportError):
                    return
                else:
                    self.variables = setup_func()
                    return

    def do_work(self, testfile):
        work = get_work(testfile, self.locust.client)
        for suite in work:
            for test in suite:
                test.testcase_dict['variables'].update(self.variables)
                test.testcase_dict['request']['group'] = test.testcase_dict['name']
                test.testcase_dict['request']['verify'] = False
                test.testcase_dict['request']['timeout'] = 30
                try:
                    test.runTest()
                except (MyBaseError, MyBaseFailure) as ex:
                    from locust.events import request_failure
                    request_failure.fire(
                        request_type=test.testcase_dict.get("request", {}).get("method"),
                        name=test.testcase_dict.get("request", {}).get("group"),
                        response_time=0,
                        exception=ex
                    )
                    break
                gevent.sleep(1)

    @task(weight=1)
    def test_any(self):
        test = random.choice(self.locust.hrun_tests)
        self.do_work(test)


class WebSiteUser(HttpLocust):
    hrun_config, hrun_tests = load_tests()
    host = hrun_config.get('request', {}).get('base_url', '')
    task_set = WebSiteTasks
    min_wait = 10
    max_wait = 10
