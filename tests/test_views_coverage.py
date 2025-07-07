"""Test for fastrunner views to improve coverage"""
import json
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from fastrunner.models import API, Case, Config, Project, Report, Variables
from fastrunner.views import api, config, project, run
from tests.test_constants import TEST_PASSWORD
from fastrunner.views import report as report_views
from fastuser.models import MyUser, UserToken


@pytest.mark.django_db
class TestProjectViews(TestCase):
    """Test project view methods"""
    
    def setUp(self):
        self.factory = RequestFactory()
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
        
    def test_project_view_single(self):
        """Test single project retrieval"""
        view = project.ProjectView()
        request = self.factory.get(f'/project/{self.project.id}/')
        request.user = self.user
        
        # Mock get_queryset
        view.get_queryset = MagicMock(return_value=Project.objects.filter(id=self.project.id))
        
        response = view.single(request, pk=self.project.id)
        self.assertEqual(response.status_code, 200)
        
    @patch('fastrunner.views.project.DashBoardView.get_week_new')
    @patch('fastrunner.views.project.DashBoardView.get_month_new')
    def test_dashboard_get(self, mock_month, mock_week):
        """Test dashboard statistics"""
        mock_week.return_value = [1, 2, 3, 4, 5, 0, 0]
        mock_month.return_value = [10] * 30
        
        view = project.DashBoardView()
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        response = view.get(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('api_count', response.data)


@pytest.mark.django_db
class TestAPIViews(TestCase):
    """Test API view methods"""
    
    def setUp(self):
        self.factory = RequestFactory()
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
        
    def test_api_single(self):
        """Test single API retrieval"""
        test_api = API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body=json.dumps({"name": "test"}),
            relation=1
        )
        
        view = api.APITemplateView()
        request = self.factory.get(f'/api/{test_api.id}/')
        request.user = self.user
        
        response = view.single(request, pk=test_api.id)
        self.assertEqual(response.status_code, 200)
        
    def test_api_list(self):
        """Test API list with pagination"""
        # Create multiple APIs
        for i in range(5):
            API.objects.create(
                name=f"Test API {i}",
                project=self.project,
                method="GET",
                url=f"/test{i}",
                body=json.dumps({"name": f"test{i}"}),
                relation=1
            )
            
        view = api.APITemplateView()
        request = self.factory.get('/api/')
        request.user = self.user
        request.query_params = {
            'project': self.project.id,
            'node': '',
            'name': '',
            'search': ''
        }
        
        # Mock paginate_queryset
        view.paginate_queryset = MagicMock(return_value=API.objects.all()[:2])
        view.get_paginated_response = MagicMock(return_value=Mock(status_code=200))
        
        response = view.list(request)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestConfigViews(TestCase):
    """Test config view methods"""
    
    def setUp(self):
        self.factory = RequestFactory()
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
        
    def test_config_all(self):
        """Test getting all configs"""
        config = Config.objects.create(
            name="Test Config",
            project=self.project,
            body=json.dumps({"name": "test"})
        )
        
        view = config.ConfigView()
        request = self.factory.get(f'/config/{config.id}/')
        request.user = self.user
        request.query_params = {'project': self.project.id}
        
        response = view.all(request, pk=config.id)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestRunViews(TestCase):
    """Test run view functions"""
    
    def setUp(self):
        self.factory = RequestFactory()
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
        
    @patch('fastrunner.views.run.run_by_single')
    def test_run_api_pk(self, mock_run):
        """Test running API by primary key"""
        mock_run.return_value = {"success": True}
        
        test_api = API.objects.create(
            name="Run API",
            project=self.project,
            method="GET",
            url="/run",
            body=json.dumps({"name": "run"}),
            relation=1
        )
        
        request = self.factory.get(f'/run_api_pk/{test_api.id}/')
        request.user = self.user
        request.query_params = {
            'config': '',
            'project': self.project.id
        }
        
        response = run.run_api_pk(request, pk=test_api.id)
        self.assertEqual(response.status_code, 200)
        
    @patch('fastrunner.views.run.run_by_batch')
    def test_run_api_tree(self, mock_run):
        """Test running API tree"""
        mock_run.return_value = {"success": True}
        
        request = self.factory.post('/run_api_tree/')
        request.user = self.user
        request.data = {
            'id': [1, 2, 3],
            'config': '',
            'project': self.project.id,
            'run_type': 'api'
        }
        
        response = run.run_api_tree(request)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestReportViews(TestCase):
    """Test report view methods"""
    
    def setUp(self):
        self.factory = RequestFactory()
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
        
    def test_report_look(self):
        """Test viewing report details"""
        report = Report.objects.create(
            project=self.project,
            name="Test Report",
            type=1,
            status=True,
            creator=self.user.username,
            detail=json.dumps({
                "success": True,
                "stat": {"total": 10, "successes": 8, "failures": 2}
            })
        )
        
        view = report_views.ReportView()
        request = self.factory.get(f'/reports/{report.id}/')
        request.user = self.user
        
        response = view.look(request, pk=report.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], report.id)


@pytest.mark.django_db
class TestViewHelpers(TestCase):
    """Test view helper methods"""
    
    def test_project_view_debugtalk(self):
        """Test debugtalk retrieval"""
        project = Project.objects.create(
            name="Debug Project",
            desc="Test",
            responsible="test"
        )
        
        view = project.DebugTalkView()
        factory = RequestFactory()
        request = factory.get(f'/debugtalk/{project.id}/')
        
        response = view.debugtalk(request, pk=project.id)
        self.assertEqual(response.status_code, 200)
        
    def test_tree_view(self):
        """Test tree view"""
        project = Project.objects.create(
            name="Tree Project",
            desc="Test",
            responsible="test"
        )
        
        view = project.TreeView()
        factory = RequestFactory()
        request = factory.get(f'/tree/{project.id}/')
        request.query_params = {'type': '1'}
        
        response = view.get(request, pk=project.id)
        self.assertEqual(response.status_code, 200)