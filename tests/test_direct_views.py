"""
Direct view testing for improved coverage
"""
import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APIRequestFactory

from fastrunner.models import API, Case, Config, Project
from fastrunner.views import api, config, project, run
from fastrunner.utils import response
from fastuser.models import MyUser, UserToken


@pytest.mark.django_db
class TestDirectViews(TestCase):
    """Test views directly for better coverage"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='viewuser',
            email='view@example.com',
            password='testpass123'
        )
        self.token = UserToken.objects.create(user=self.user, token='view-token')
        
        self.project = Project.objects.create(
            name="View Test Project",
            desc="Test project",
            responsible="viewuser"
        )

    def test_project_view_single(self):
        """Test ProjectView single method"""
        view = project.ProjectView()
        view.get_queryset = MagicMock(return_value=Project.objects.filter(id=self.project.id))
        
        request = self.factory.get(f'/api/fastrunner/project/{self.project.id}/')
        request.user = self.user
        
        response_data = view.single(request, pk=self.project.id)
        self.assertEqual(response_data.status_code, 200)

    def test_api_template_view_single(self):
        """Test APITemplateView single method"""
        test_api = API.objects.create(
            name="Test API",
            project=self.project,
            method="GET", 
            url="/test",
            body=json.dumps({"name": "test"})
        )
        
        view = api.APITemplateView()
        request = self.factory.get(f'/api/fastrunner/api/{test_api.id}/')
        request.user = self.user
        
        response_data = view.single(request, pk=test_api.id)
        self.assertEqual(response_data.status_code, 200)

    def test_config_view_all(self):
        """Test ConfigView all method"""
        test_config = Config.objects.create(
            name="Test Config",
            project=self.project,
            body=json.dumps({"name": "test"})
        )
        
        view = config.ConfigView()
        request = self.factory.get(f'/api/fastrunner/config/{test_config.id}/')
        request.user = self.user
        request.query_params = {"project": self.project.id}
        
        response_data = view.all(request, pk=test_config.id)
        self.assertEqual(response_data.status_code, 200)


@pytest.mark.django_db
class TestResponseUtils(TestCase):
    """Test all response utilities"""

    def test_all_response_codes(self):
        """Test all response code constants"""
        # Success responses
        self.assertEqual(response.SYSTEM_SUCCESS['code'], '0001')
        self.assertEqual(response.PROJECT_ADD_SUCCESS['code'], '0001')
        self.assertEqual(response.PROJECT_UPDATE_SUCCESS['code'], '0001')
        self.assertEqual(response.TREE_UPDATE_SUCCESS['code'], '0001')
        self.assertEqual(response.API_ADD_SUCCESS['code'], '0001')
        
        # Error responses
        self.assertEqual(response.SYSTEM_ERROR['code'], '9999')
        self.assertEqual(response.VALIDATE_ERROR['code'], '9998')
        self.assertEqual(response.AUTH_FAIL['code'], '9997')
        self.assertEqual(response.DATA_TO_LONG['code'], '0002')
        self.assertEqual(response.FILE_UPLOAD_ERROR['code'], '0003')
        
        # Check success flags
        self.assertTrue(response.SYSTEM_SUCCESS['success'])
        self.assertFalse(response.SYSTEM_ERROR['success'])
        self.assertFalse(response.VALIDATE_ERROR['success'])


@pytest.mark.django_db
class TestRunViews(TestCase):
    """Test run view functions"""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            username='runuser',
            email='run@example.com',
            password='testpass123'
        )
        
        self.project = Project.objects.create(
            name="Run Test Project",
            desc="Test project",
            responsible="runuser"
        )
        
        self.config = Config.objects.create(
            name="Test Config",
            project=self.project,
            body=json.dumps({
                "name": "Test Config",
                "request": {"base_url": "http://test.com"}
            })
        )

    @patch('fastrunner.views.run.run_by_single')
    def test_run_api_pk(self, mock_run):
        """Test run_api_pk function"""
        mock_run.return_value = {"success": True}
        
        test_api = API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body=json.dumps({"name": "test"})
        )
        
        request = self.factory.get(f'/api/fastrunner/run_api_pk/{test_api.id}/', {
            'config': self.config.id,
            'project': self.project.id
        })
        request.user = self.user
        
        response_data = run.run_api_pk(request, pk=test_api.id)
        self.assertEqual(response_data.status_code, 200)

    @patch('fastrunner.views.run.run_by_batch')
    def test_run_api_tree(self, mock_run):
        """Test run_api_tree function"""
        mock_run.return_value = {"success": True}
        
        request = self.factory.post('/api/fastrunner/run_api_tree/', {
            'id': [1, 2, 3],
            'config': self.config.id,
            'project': self.project.id
        })
        request.user = self.user
        request.data = request.POST
        
        response_data = run.run_api_tree(request)
        self.assertEqual(response_data.status_code, 200)


@pytest.mark.django_db
class TestUtilityFunctions(TestCase):
    """Test various utility functions"""

    def test_loader_functions(self):
        """Test loader utility functions"""
        from fastrunner.utils.loader import save_summary
        
        # Test save_summary
        summary = {
            "success": True,
            "stat": {"total": 5, "successes": 4, "failures": 1}
        }
        
        result = save_summary("test_name", summary, project_id=1, type=1)
        self.assertIsNotNone(result)

    def test_prepare_functions(self):
        """Test prepare utility functions"""
        from fastrunner.utils.prepare import generate_testcase, get_counter
        
        # Test get_counter
        counter = get_counter("${var}", ["var"])
        self.assertEqual(counter, {"var": 1})
        
        # Test with no variables
        counter = get_counter("plain text", [])
        self.assertEqual(counter, {})


@pytest.mark.django_db
class TestTaskUtils(TestCase):
    """Test task utility functions"""

    @patch('fastrunner.utils.task.send_message_dingding')
    @patch('fastrunner.utils.task.send_message_lark')
    @patch('fastrunner.utils.task.send_message_qywx')
    def test_async_send_msg(self, mock_qywx, mock_lark, mock_ding):
        """Test async message sending"""
        from fastrunner.utils.task import async_send_msg
        
        # Test with dingding
        msg_dict = {
            "msg_name": "Test",
            "msg_type": "dingding",
            "webhook": "https://test.com/hook",
            "summary": {"total": 10, "success": 8}
        }
        
        async_send_msg(**msg_dict)
        mock_ding.assert_called_once()
        
        # Test with lark
        msg_dict["msg_type"] = "lark"
        async_send_msg(**msg_dict)
        mock_lark.assert_called_once()
        
        # Test with qywx
        msg_dict["msg_type"] = "qywx"
        async_send_msg(**msg_dict)
        mock_qywx.assert_called_once()