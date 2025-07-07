"""Test for fastrunner views with proper mocking"""
import json
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from test_constants import TEST_PASSWORD

from fastrunner.models import API, Case, Config, Project, Report, ReportDetail, Variables
from fastrunner.views import api, config, project, run
from fastrunner.views import report as report_views
from fastuser.models import MyUser, UserToken


def mock_request_log(func):
    """Mock request_log decorator to bypass WSGIRequest issues"""
    return func


@pytest.mark.django_db
class TestProjectViewsProper(TestCase):
    """Test project view methods with proper mocking"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test",
            responsible="testuser"
        )
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_project_view_single(self):
        """Test single project retrieval"""
        from fastrunner.views.project import ProjectView
        
        request = self.factory.get(f'/api/project/{self.project.id}/')
        request.user = self.user
        
        view = ProjectView()
        response = view.single(request, pk=self.project.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.project.id)
        self.assertEqual(response.data['name'], 'Test Project')
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_dashboard_get(self):
        """Test dashboard statistics"""
        from fastrunner.views.project import DashBoardView
        
        # Create test data
        API.objects.create(
            name="Dashboard API",
            project=self.project,
            method="GET",
            url="/api/test",
            body=json.dumps({"name": "Test"}),
            relation=1
        )
        
        Case.objects.create(
            name="Dashboard Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        Report.objects.create(
            project=self.project,
            name="Dashboard Report",
            type=1,
            status=True,
            summary=json.dumps({"success": True})
        )
        
        request = self.factory.get('/api/dashboard/')
        request.user = self.user
        
        view = DashBoardView()
        response = view.get(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('api_count', response.data)
        self.assertIn('case_count', response.data)
        self.assertIn('report_count', response.data)
        self.assertIn('fail_count', response.data)


@pytest.mark.django_db
class TestAPIViewsProper(TestCase):
    """Test API view methods with proper mocking"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="API Project",
            desc="Test",
            responsible="apiuser"
        )
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_api_single(self):
        """Test single API retrieval"""
        from fastrunner.views.api import APITemplateView
        
        api_obj = API.objects.create(
            name="Single API",
            project=self.project,
            method="GET",
            url="/api/single",
            body=json.dumps({"name": "Single API"}),
            relation=1
        )
        
        request = self.factory.get(f'/api/template/{api_obj.id}/')
        request.user = self.user
        
        view = APITemplateView()
        response = view.single(request, pk=api_obj.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], api_obj.id)
        self.assertEqual(response.data['name'], 'Single API')
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_api_list(self):
        """Test API list with pagination"""
        from fastrunner.views.api import APITemplateView
        
        # Create multiple APIs
        for i in range(15):
            API.objects.create(
                name=f"API {i}",
                project=self.project,
                method="GET",
                url=f"/api/test{i}",
                body=json.dumps({"name": f"API {i}"}),
                relation=1
            )
        
        request = self.factory.get('/api/template/')
        request.user = self.user
        request.query_params = {'node': 1, 'project': self.project.id, 'search': ''}
        
        view = APITemplateView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertGreater(len(response.data['results']), 0)


@pytest.mark.django_db
class TestConfigViewsProper(TestCase):
    """Test config view methods with proper mocking"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='configuser',
            email='config@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Config Project",
            desc="Test",
            responsible="configuser"
        )
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_config_all(self):
        """Test getting all configs"""
        from fastrunner.views.config import ConfigView
        
        # Create configs
        Config.objects.create(
            name="Config 1",
            project=self.project,
            body=json.dumps({"name": "Config 1"})
        )
        Config.objects.create(
            name="Config 2",
            project=self.project,
            body=json.dumps({"name": "Config 2"})
        )
        
        request = self.factory.get('/api/config/')
        request.user = self.user
        request.query_params = {'project': self.project.id}
        
        view = ConfigView()
        response = view.all(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)


@pytest.mark.django_db
class TestRunViewsProper(TestCase):
    """Test run view functions with proper authentication"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='runuser',
            email='run@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Run Project",
            desc="Test",
            responsible="runuser"
        )
        
        self.config = Config.objects.create(
            name="Run Config",
            project=self.project,
            body=json.dumps({
                "name": "Run Config",
                "request": {"base_url": "http://localhost:8000"}
            })
        )
        
        self.api = API.objects.create(
            name="Run API",
            project=self.project,
            method="GET",
            url="/api/run",
            body=json.dumps({
                "name": "Run API",
                "request": {"url": "/api/run", "method": "GET"}
            }),
            relation=1
        )
        
    @patch('fastrunner.utils.loader.debug_api')
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_run_api_pk(self):
        """Test running API by primary key"""
        from fastrunner.views.run import run_api_pk
        
        # Mock debug_api to return success
        with patch('fastrunner.utils.loader.debug_api') as mock_debug:
            mock_debug.return_value = {
                "success": True,
                "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
            }
            
            request = self.factory.get(f'/api/run_api_pk/{self.api.id}/')
            request.user = self.user
            request.query_params = {
                'config': self.config.name,
                'project': self.project.id,
                'host': 'http://localhost:8000'
            }
            
            response = run_api_pk(request, pk=self.api.id)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.data['success'])
        
    @patch('fastrunner.utils.loader.debug_api')
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_run_api_tree(self):
        """Test running API tree"""
        from fastrunner.views.run import run_api_tree
        
        with patch('fastrunner.utils.loader.debug_api') as mock_debug:
            mock_debug.return_value = {
                "success": True,
                "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
            }
            
            request = self.factory.post('/api/run_api_tree/')
            request.user = self.user
            request.data = {
                'id': [self.api.id],
                'config': self.config.name,
                'project': self.project.id,
                'run_type': 'api'
            }
            
            response = run_api_tree(request)
            
            self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestReportViewsProper(TestCase):
    """Test report view methods with proper mocking"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='reportuser',
            email='report@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Report Project",
            desc="Test",
            responsible="reportuser"
        )
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_report_look(self):
        """Test viewing report details"""
        from fastrunner.views.report import ReportView
        
        report = Report.objects.create(
            project=self.project,
            name="Look Report",
            type=1,
            status=True,
            summary=json.dumps({
                "success": True,
                "stat": {"testcases": {"total": 10, "success": 10, "fail": 0}}
            })
        )
        
        ReportDetail.objects.create(
            report=report,
            summary_detail=json.dumps({
                "details": [{"name": "test", "success": True}]
            })
        )
        
        request = self.factory.get(f'/api/report/{report.id}/')
        request.user = self.user
        
        view = ReportView()
        response = view.look(request, pk=report.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], report.id)
        self.assertIn('detail', response.data)


@pytest.mark.django_db
class TestViewHelpersProper(TestCase):
    """Test view helper methods with proper mocking"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='helperuser',
            email='helper@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Helper Project",
            desc="Test",
            responsible="helperuser"
        )
    
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_project_view_debugtalk(self):
        """Test debugtalk retrieval"""
        from fastrunner.views.project import DebugTalkView
        
        request = self.factory.get(f'/api/debugtalk/{self.project.id}/')
        request.user = self.user
        
        view = DebugTalkView()
        response = view.debugtalk(request, pk=self.project.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('debugtalk', response.data)
        
    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_tree_view(self):
        """Test tree view"""
        from fastrunner.views.project import TreeView
        
        # Create relation for tree
        from fastrunner.models import Relation
        Relation.objects.create(
            project=self.project,
            tree=json.dumps([{"id": 1, "label": "Root", "children": []}]),
            type=1
        )
        
        request = self.factory.get(f'/api/tree/{self.project.id}/')
        request.user = self.user
        request.query_params = {'type': '1'}
        
        view = TreeView()
        response = view.get(request, pk=self.project.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)