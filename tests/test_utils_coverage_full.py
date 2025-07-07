"""Test for various util modules to achieve 100% coverage"""
import json
import os
from datetime import datetime
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest
from django.test import TestCase

from fastrunner.models import Project, Report
from fastrunner.utils import (
    convert2boomer,
    convert2hrp,
    day,
    ding_message,
    email_helper,
    lark_message,
    middleware,
    parser,
    prepare,
    runner,
    task,
)


@pytest.mark.django_db
class TestConvert2Boomer(TestCase):
    """Test convert2boomer module"""
    
    def test_gen_boomer_api(self):
        """Test gen_boomer function for API"""
        apis = [{
            "name": "Test API",
            "request": {
                "url": "/api/test",
                "method": "GET",
                "headers": {"Content-Type": "application/json"}
            },
            "validate": [
                {"eq": ["status_code", 200]}
            ]
        }]
        
        result = convert2boomer.gen_boomer(apis, type="api")
        
        self.assertIn("from locust import HttpUser", result)
        self.assertIn("class User(HttpUser):", result)
        self.assertIn("def test_api(self):", result)

    def test_gen_boomer_case(self):
        """Test gen_boomer function for case"""
        cases = [{
            "testcases": [{
                "name": "Test Case",
                "request": {
                    "url": "/api/case",
                    "method": "POST",
                    "json": {"test": "data"}
                }
            }]
        }]
        
        result = convert2boomer.gen_boomer(cases, type="case")
        
        self.assertIn("from locust import HttpUser", result)
        self.assertIn("def test_case(self):", result)


@pytest.mark.django_db
class TestConvert2HRP(TestCase):
    """Test convert2hrp module"""
    
    def test_generate_hrp_case_api(self):
        """Test generate_hrp_case for API"""
        api = {
            "name": "HRP API",
            "request": {
                "url": "/hrp/api",
                "method": "GET",
                "headers": {"Authorization": "Bearer token"}
            },
            "validate": [
                {"eq": ["status_code", 200]},
                {"contains": ["body", "success"]}
            ],
            "extract": [
                {"token": "body.token"}
            ]
        }
        
        result = convert2hrp.generate_hrp_case(api, type="api")
        
        self.assertIn("config", result)
        self.assertIn("teststeps", result)
        self.assertEqual(len(result["teststeps"]), 1)
        step = result["teststeps"][0]
        self.assertEqual(step["name"], "HRP API")
        self.assertIn("validate", step)
        self.assertIn("extract", step)

    def test_generate_hrp_case_case(self):
        """Test generate_hrp_case for case"""
        case = {
            "testcases": [{
                "name": "HRP Case",
                "request": {
                    "url": "/hrp/case",
                    "method": "POST",
                    "json": {"data": "test"}
                },
                "setup_hooks": ["${setup()}"],
                "teardown_hooks": ["${teardown()}"]
            }]
        }
        
        result = convert2hrp.generate_hrp_case(case, type="case")
        
        self.assertIn("config", result)
        self.assertIn("teststeps", result)
        step = result["teststeps"][0]
        self.assertIn("testcase", step)

    def test_parse_hooks(self):
        """Test parse_hooks function"""
        hooks = ["${func1()}", "${func2(a, b)}"]
        result = convert2hrp.parse_hooks(hooks)
        self.assertEqual(result, ["func1()", "func2(a, b)"])
        
        # Test with empty hooks
        result = convert2hrp.parse_hooks([])
        self.assertEqual(result, [])
        
        # Test with None
        result = convert2hrp.parse_hooks(None)
        self.assertEqual(result, [])

    def test_gen_hrp_case_from_json(self):
        """Test gen_hrp_case_from_json function"""
        json_data = {
            "teststeps": [{
                "name": "Step 1",
                "request": {"url": "/test", "method": "GET"}
            }]
        }
        
        result = convert2hrp.gen_hrp_case_from_json(json.dumps(json_data))
        
        self.assertIsInstance(result, dict)
        self.assertIn("teststeps", result)

    def test_gen_raw_hrp_case(self):
        """Test gen_raw_hrp_case function"""
        raw_str = '''
        config:
          name: Test
        teststeps:
        - name: Step1
          request:
            url: /test
            method: GET
        '''
        
        result = convert2hrp.gen_raw_hrp_case(raw_str, type="case")
        
        self.assertIn("config", result)
        self.assertIn("teststeps", result)


@pytest.mark.django_db
class TestDayUtils(TestCase):
    """Test day utility module"""
    
    def test_get_month(self):
        """Test get_month function"""
        result = day.get_month()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("categories", result[0])
        self.assertIn("data", result[0])

    def test_get_weeks(self):
        """Test get_weeks function"""
        result = day.get_weeks()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("categories", result[0])
        self.assertIn("data", result[0])

    @patch('fastrunner.models.Report.objects.filter')
    def test_get_month_with_data(self, mock_filter):
        """Test get_month with report data"""
        # Mock report data
        mock_report = Mock()
        mock_report.update_time = datetime.now()
        mock_filter.return_value = [mock_report]
        
        result = day.get_month()
        
        # Should still return proper structure
        self.assertEqual(len(result), 2)


@pytest.mark.django_db
class TestDingMessage(TestCase):
    """Test DingTalk message module"""
    
    @patch('requests.post')
    def test_send_ding_msg(self, mock_post):
        """Test send_ding_msg function"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errcode": 0}
        mock_post.return_value = mock_response
        
        ding = ding_message.DingMessage(webhook="https://oapi.dingtalk.com/robot/send")
        
        summary = {
            "stat": {
                "testcases": {"total": 10, "success": 8, "fail": 2}
            },
            "time": {
                "start_at": "2023-12-25T10:00:00",
                "duration": 60.5
            }
        }
        
        ding.send_ding_msg(summary)
        
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("msgtype", call_args[1]["json"])


@pytest.mark.django_db
class TestLarkMessage(TestCase):
    """Test Lark message module"""
    
    @patch('requests.post')
    def test_send_message(self, mock_post):
        """Test send_message function"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0}
        mock_post.return_value = mock_response
        
        summary = {
            "stat": {
                "testcases": {"total": 10, "success": 9, "fail": 1}
            },
            "time": {
                "start_at": "2023-12-25T10:00:00",
                "duration": 45.2
            },
            "task_name": "Test Task",
            "report_id": 123
        }
        
        lark_message.send_message(summary, "https://open.feishu.cn/hook/xxx", 5)
        
        mock_post.assert_called_once()


@pytest.mark.django_db
class TestEmailHelper(TestCase):
    """Test email helper module"""
    
    @patch('django.core.mail.send_mail')
    def test_send_email_report(self, mock_send_mail):
        """Test send_email_report function"""
        mock_send_mail.return_value = 1
        
        result = email_helper.send_email_report(
            "test@example.com",
            "http://example.com/report/123"
        )
        
        mock_send_mail.assert_called_once()
        self.assertTrue(result)


@pytest.mark.django_db
class TestMiddleware(TestCase):
    """Test middleware module"""
    
    def test_exception_middleware(self):
        """Test ExceptionMiddleware"""
        get_response = Mock()
        get_response.return_value = Mock(status_code=200)
        
        middleware_instance = middleware.ExceptionMiddleware(get_response)
        
        request = Mock()
        response = middleware_instance(request)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.models.Visit.objects.create')
    def test_visit_times_middleware(self, mock_create):
        """Test VisitTimesMiddleware"""
        get_response = Mock()
        get_response.return_value = Mock(status_code=200)
        
        middleware_instance = middleware.VisitTimesMiddleware(get_response)
        
        request = Mock()
        request.user = Mock(username="testuser")
        request.META = {
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET'
        }
        request.path = '/api/test'
        request.body = b'{}'
        
        response = middleware_instance(request)
        
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestParserAdvanced(TestCase):
    """Test parser module advanced features"""
    
    def test_format_json(self):
        """Test Format class with JSON data"""
        data = {
            "name": "Test",
            "project": 1,
            "relation": 1,
            "method": "POST",
            "url": "/api/test",
            "request": {
                "json": {"key": "value"},
                "params": {"param1": "value1"},
                "headers": {"header": {"Content-Type": "application/json"}}
            },
            "validate": [
                {"equals": ["status_code", 200]}
            ],
            "extract": [
                {"token": {"jsonpath": "$.data.token"}}
            ]
        }
        
        formatter = parser.Format(data)
        formatter.parse()
        
        self.assertIsNotNone(formatter.testcase)
        self.assertIn("request", formatter.testcase)
        self.assertIn("validate", formatter.testcase)

    def test_format_form_data(self):
        """Test Format class with form data"""
        data = {
            "name": "Form Test",
            "project": 1,
            "method": "POST",
            "url": "/api/form",
            "request": {
                "data": {"field1": "value1", "field2": "value2"},
                "files": {"file": "test.txt"}
            }
        }
        
        formatter = parser.Format(data)
        formatter.parse()
        
        self.assertIn("data", formatter.testcase["request"])

    def test_format_config(self):
        """Test config formatting"""
        config_data = {
            "config": {
                "name": "Test Config",
                "base_url": "http://example.com",
                "variables": {"var1": "value1"},
                "parameters": {"param1": "value1"},
                "verify": False,
                "export": ["var1"],
                "weight": 100
            }
        }
        
        result = parser.format_json(config_data)
        
        self.assertIn("config", result)
        self.assertIn("variables", result["config"])

    def test_format_testcase(self):
        """Test testcase formatting"""
        testcase = {
            "test": {
                "name": "Test Case",
                "api": "api_name",
                "testcase": "testcase_name",
                "variables": {"var": "value"},
                "validate": [{"eq": ["status_code", 200]}],
                "extract": {"token": "body.token"},
                "setup_hooks": ["${setup()}"],
                "teardown_hooks": ["${teardown()}"]
            }
        }
        
        result = parser.format_json(testcase)
        
        self.assertIn("test", result)
        self.assertIn("validate", result["test"])


@pytest.mark.django_db
class TestPrepareAdvanced(TestCase):
    """Test prepare module advanced features"""
    
    def test_project_init(self):
        """Test project_init function"""
        project = Project.objects.create(
            name="Prepare Project",
            desc="Test",
            responsible="test"
        )
        
        result = prepare.project_init(project)
        
        self.assertIn("tree", result[0])
        self.assertIsInstance(result[0]["tree"], list)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='def helper(): pass')
    def test_generate_testcase_file(self, mock_file, mock_exists):
        """Test generate_testcase_file function"""
        mock_exists.return_value = True
        
        body = [{
            "name": "Test",
            "request": {"url": "/test", "method": "GET"}
        }]
        
        with patch('shutil.rmtree'):
            result = prepare.generate_testcase_file(body, env_path="/tmp/test")
            
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_get_total_values(self):
        """Test get_total_values function"""
        total_str = '{"var1": "value1", "var2": "value2"}'
        
        result = prepare.get_total_values(total_str)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn({"var1": "value1"}, result)


@pytest.mark.django_db
class TestRunnerAdvanced(TestCase):
    """Test runner module advanced features"""
    
    def test_debug_code_init(self):
        """Test DebugCode initialization"""
        code = '''
def setup():
    print("Setup")
    
def teardown():
    print("Teardown")
'''
        
        debug = runner.DebugCode(code)
        
        self.assertTrue(debug.temp.startswith('/tmp/FasterRunner'))
        self.assertTrue(os.path.exists(debug.temp))
        
        # Clean up
        debug.__del__()

    @patch('os.system')
    def test_run_by_httprunner(self, mock_system):
        """Test RunByHttpRunner class"""
        mock_system.return_value = 0
        
        case_path = "/tmp/test_case.yml"
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='{"success": true}')):
                runner_instance = runner.RunByHttpRunner(case_path)
                result = runner_instance.run()
                
                self.assertIsInstance(result, dict)


@pytest.mark.django_db
class TestTaskUtils(TestCase):
    """Test task utility module"""
    
    @patch('django_celery_beat.models.CrontabSchedule.objects.create')
    def test_create_task(self, mock_create):
        """Test create_task function"""
        mock_crontab = Mock(id=1)
        mock_create.return_value = mock_crontab
        
        with patch('django_celery_beat.models.PeriodicTask.objects.create') as mock_task_create:
            mock_task = Mock(name='test_task')
            mock_task_create.return_value = mock_task
            
            kwargs = {
                'name': 'Test Task',
                'crontab': '0 0 * * *',
                'switch': True,
                'data': [1, 2, 3]
            }
            
            result = task.create_task(**kwargs)
            
            self.assertEqual(result['name'], 'test_task')

    @patch('django_celery_beat.models.PeriodicTask.objects.get')
    def test_delete_task(self, mock_get):
        """Test delete_task function"""
        mock_task = Mock()
        mock_get.return_value = mock_task
        
        result = task.delete_task('test_task')
        
        self.assertEqual(result, {'msg': '删除成功'})
        mock_task.delete.assert_called_once()

    @patch('django_celery_beat.models.PeriodicTask.objects.get')
    def test_change_task_status(self, mock_get):
        """Test change_task_status function"""
        mock_task = Mock()
        mock_task.enabled = False
        mock_get.return_value = mock_task
        
        result = task.change_task_status('test_task', True)
        
        self.assertEqual(result, {'msg': '更新成功'})
        self.assertTrue(mock_task.enabled)
        mock_task.save.assert_called_once()

    def test_get_crontab_next_execute_time(self):
        """Test get_crontab_next_execute_time function"""
        crontab = '0 10 * * *'  # Daily at 10:00
        
        result = task.get_crontab_next_execute_time(crontab)
        
        self.assertIsInstance(result, str)
        self.assertIn(':', result)  # Should contain time format