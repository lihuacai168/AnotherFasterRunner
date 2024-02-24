import random

from httprunner.exceptions import MyBaseError, MyBaseFailure
from httprunner.loader import load_locust_tests
from httprunner.runner import Runner
from locust import HttpLocust, TaskSet, task
from locust.events import request_failure


class WebPageTasks(TaskSet):
    def on_start(self):
        self.test_runner = Runner(self.client)
        self.testcases = loader.load_locust_tests(self.locust.file_path)

    @task(weight=1)
    def test_any(self):
        teststeps = random.choice(self.locust.tests)
        for teststep in teststeps:
            try:
                test_runner.run_test(teststep)
            except (MyBaseError, MyBaseFailure) as ex:
                request_failure.fire(
                    request_type=teststep.get("request", {}).get("method"),
                    name=teststep.get("name"),
                    response_time=0,
                    exception=ex
                )
                break
            gevent.sleep(1)


class WebPageUser(HttpLocust):
    host = "$HOST"
    task_set = WebPageTasks
    min_wait = 10
    max_wait = 30

    # file_path = "$TESTCASE_FILE"
    file_path = "tests/data/demo_locust.yml"
    config, tests = load_locust_tests(file_path)
