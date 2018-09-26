
import os, django





os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FasterRunner.settings")  # project_name 项目名称
django.setup()

from fastrunner import models
from httprunner import HttpRunner, logger

import time


a =1
def time_cmp(first_time, second_time):
    """
    time
    """
    return int(time.strftime("%Y-%m-%d %H:%M:%S", first_time))

def time_sleep(time):
    time.sleep(time)
def parse_tests(testcases, config=None):
    """get test case structure
    """
    testcases = {
        "teststeps": testcases,
    }

    if config:
        testcases["config"] = config

    return testcases

if __name__ == '__main__':
    import json
    logger.setup_logger('DEBUG')
    def debug_api(api_id, config_id=None):
        """debug api
            api_id :int
            config_id: int
        """
        config_body = None

        if config_id:
            config = models.Config.objects.get(id=config_id)
            config_body = json.loads(config.body)

        test = models.API.objects.get(id=api_id)
        test_body = [eval(test.body)]

        testcase_list = [parse_tests(test_body, config=config_body)]
        kwargs = {
            "failfast": False
        }

        runner = HttpRunner(**kwargs)
        runner.run(testcase_list)
        runner.gen_html_report()
        return runner.summary

    summary = debug_api(122)



