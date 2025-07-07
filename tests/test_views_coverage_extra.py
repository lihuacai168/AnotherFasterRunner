"""Test for fastrunner.views modules to improve coverage"""
import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.test import TestCase
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework.test import APIRequestFactory
from test_constants import TEST_PASSWORD

from fastrunner.models import API, Case, CaseStep, Config, Project, Report, ReportDetail, Variables
from fastrunner.views import ci, schedule, suite, timer_task, yapi
from fastuser.models import MyUser


def mock_request_log(func):
    """Mock request_log decorator"""
    return func


@pytest.mark.django_db
class TestCIViews(TestCase):
    """Test CI views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='ciuser',
            email='ci@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="CI Project",
            desc="Test",
            responsible="ciuser"
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_ci_run_tests_get(self, mock_debug):
        """Test CI run tests GET method"""
        from fastrunner.views.ci import CIRunTests
        
        request = self.factory.get('/api/ci/run_tests/')
        request.user = self.user
        
        view = CIRunTests()
        response = view.get(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], "CI backend service is OK!")

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.views.ci.async_debug_suite.delay')
    def test_ci_run_tests_post(self, mock_async_debug):
        """Test CI run tests POST method"""
        from fastrunner.views.ci import CIRunTests
        
        # Create test case
        case = Case.objects.create(
            name="CI Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        ci_data = {
            "ci_job_id": 123,
            "ci_job_url": "http://gitlab.example.com/job/123",
            "ci_pipeline_id": 456,
            "ci_pipeline_url": "http://gitlab.example.com/pipeline/456",
            "ci_project_id": 789,
            "ci_project_name": "test-project",
            "ci_project_namespace": "test-namespace",
            "env": "test",
            "start_job_user": "ci_user",
            "run_cases": json.dumps([case.id]),
            "config": "测试环境"
        }
        
        request = self.factory.post('/api/ci/run_tests/', ci_data)
        request.user = self.user
        
        view = CIRunTests()
        response = view.post(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], "触发成功")
        mock_async_debug.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_get_ci_project_detail(self):
        """Test get CI project detail"""
        from fastrunner.views.ci import get_ci_project_detail
        
        # Create report with CI metadata
        report = Report.objects.create(
            project=self.project,
            name="CI_gitlab_job_123",
            type=1,
            status=True,
            ci_metadata=json.dumps({
                "ci_job_id": 123,
                "ci_project_name": "test-project"
            }),
            summary=json.dumps({"success": True})
        )
        
        request = self.factory.get('/api/ci/project_detail/')
        request.user = self.user
        request.query_params = {'ci_id': 123}
        
        response = get_ci_project_detail(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


@pytest.mark.django_db
class TestScheduleViews(TestCase):
    """Test schedule views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='scheduser',
            email='sched@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Schedule Project",
            desc="Test",
            responsible="scheduser"
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_schedule_list(self):
        """Test ScheduleView list method"""
        from fastrunner.views.schedule import ScheduleView
        
        # Create crontab and periodic task
        crontab = CrontabSchedule.objects.create(
            minute='0',
            hour='*/2',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        )
        
        task = PeriodicTask.objects.create(
            crontab=crontab,
            name='test_schedule_task',
            task='fastrunner.tasks.schedule_debug_suite',
            enabled=True,
            kwargs=json.dumps({
                "project": self.project.id,
                "config": "test"
            })
        )
        
        request = self.factory.get('/api/schedule/')
        request.user = self.user
        request.query_params = {
            'project': self.project.id,
            'search': ''
        }
        
        view = ScheduleView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.views.schedule.create_task')
    def test_schedule_add(self, mock_create_task):
        """Test ScheduleView add method"""
        from fastrunner.views.schedule import ScheduleView
        
        mock_create_task.return_value = {"name": "new_task"}
        
        # Create test case
        case = Case.objects.create(
            name="Schedule Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        request = self.factory.post('/api/schedule/')
        request.user = self.user
        request.data = {
            "name": "Test Schedule",
            "data": [case.id],
            "crontab": "0 0 * * *",
            "switch": True,
            "task_type": "schedule",
            "project": self.project.id,
            "config": "",
            "webhook": "https://open.feishu.cn/hook/test",
            "run_type": "test"
        }
        
        view = ScheduleView()
        response = view.add(request)
        
        self.assertEqual(response.status_code, 200)
        mock_create_task.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.views.schedule.change_task_status')
    def test_schedule_update(self, mock_change_status):
        """Test ScheduleView update method"""
        from fastrunner.views.schedule import ScheduleView
        
        request = self.factory.patch('/api/schedule/')
        request.user = self.user
        request.data = {
            "id": 1,
            "switch": False
        }
        
        view = ScheduleView()
        response = view.update(request)
        
        self.assertEqual(response.status_code, 200)
        mock_change_status.assert_called_once_with(name=1, status=False)


@pytest.mark.django_db
class TestSuiteViews(TestCase):
    """Test suite views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='suiteuser',
            email='suite@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Suite Project",
            desc="Test",
            responsible="suiteuser"
        )
        self.case = Case.objects.create(
            name="Suite Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_test_list(self):
        """Test TestCaseListView list method"""
        from fastrunner.views.suite import TestCaseListView
        
        request = self.factory.get('/api/test/')
        request.user = self.user
        request.query_params = {
            'project': self.project.id,
            'node': 1,
            'search': ''
        }
        
        view = TestCaseListView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_test_add(self):
        """Test TestCaseListView add method"""
        from fastrunner.views.suite import TestCaseListView
        
        request = self.factory.post('/api/test/')
        request.user = self.user
        request.data = {
            "name": "New Test Case",
            "project": self.project.id,
            "relation": 1,
            "tag": 1
        }
        
        view = TestCaseListView()
        response = view.add(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_test_update(self):
        """Test TestCaseListView update method"""
        from fastrunner.views.suite import TestCaseListView
        
        request = self.factory.patch(f'/api/test/{self.case.id}/')
        request.user = self.user
        request.data = {
            "name": "Updated Case Name",
            "desc": "Updated description"
        }
        
        view = TestCaseListView()
        response = view.update(request, pk=self.case.id)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_test_case_step_list(self):
        """Test CaseStepView list method"""
        from fastrunner.views.suite import CaseStepView
        
        # Create case step
        CaseStep.objects.create(
            case=self.case,
            name="Test Step",
            step=1,
            body=json.dumps({"name": "Test Step"}),
            url="/test",
            method="GET"
        )
        
        request = self.factory.get(f'/api/teststep/{self.case.id}/')
        request.user = self.user
        
        view = CaseStepView()
        response = view.list(request, pk=self.case.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_test_case_step_add(self):
        """Test CaseStepView add method"""
        from fastrunner.views.suite import CaseStepView
        
        api = API.objects.create(
            name="Step API",
            project=self.project,
            method="POST",
            url="/api/step",
            body=json.dumps({"name": "Step API"}),
            relation=1
        )
        
        request = self.factory.post(f'/api/teststep/{self.case.id}/')
        request.user = self.user
        request.data = {
            "name": "New Step",
            "api": api.id,
            "step": 2,
            "body": api.body,
            "source_api_id": api.id
        }
        
        view = CaseStepView()
        response = view.add(request, pk=self.case.id)
        
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestTimerTaskViews(TestCase):
    """Test timer task views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='timeruser',
            email='timer@example.com',
            password=TEST_PASSWORD
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.views.timer_task.get_crontab_next_execute_time')
    def test_crontab_next_execute_time(self, mock_get_time):
        """Test get_next_execute_time function"""
        from fastrunner.views.timer_task import get_next_execute_time
        
        mock_get_time.return_value = "2023-12-25 10:00:00"
        
        request = self.factory.get('/api/next_execute_time/')
        request.user = self.user
        request.query_params = {'crontab': '0 10 * * *'}
        
        response = get_next_execute_time(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['next_execute_time'], "2023-12-25 10:00:00")


@pytest.mark.django_db
class TestYapiViews(TestCase):
    """Test YAPI views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='yapiuser',
            email='yapi@example.com',
            password=TEST_PASSWORD
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('requests.get')
    def test_yapi_import_view(self, mock_requests_get):
        """Test YAPIView import method"""
        from fastrunner.views.yapi import YAPIView
        
        # Mock YAPI response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "errcode": 0,
            "data": {
                "_id": 123,
                "title": "Test API",
                "path": "/api/test",
                "method": "GET",
                "req_headers": [],
                "req_query": [],
                "req_body_other": "",
                "res_body": '{"code": 0, "data": {}}'
            }
        }
        mock_requests_get.return_value = mock_response
        
        request = self.factory.post('/api/yapi/')
        request.user = self.user
        request.data = {
            "project_id": 1,
            "node_id": 1,
            "token": "test_token",
            "yapi_id": 123,
            "yapi_base_url": "http://yapi.example.com"
        }
        
        view = YAPIView()
        response = view.post(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])