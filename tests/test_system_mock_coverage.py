"""Test for system and mock modules to achieve 100% coverage"""
import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from test_constants import TEST_PASSWORD

from fastrunner.models import Project
from fastuser.models import MyUser
from mock.models import MockAPI, MockProject
from mock.serializers import MockAPISerializer, MockProjectSerializer
from mock.views import MockAPIView, MockProjectView, MockResponseView, get_req_json
from system.models import LogRecord
from system.serializers import LogRecordSerializer
from system.views import LogRecordViewSet


def mock_request_log(func):
    """Mock request_log decorator"""
    return func


@pytest.mark.django_db
class TestSystemModule(TestCase):
    """Test system module"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='systemuser',
            email='system@example.com',
            password=TEST_PASSWORD
        )

    def test_log_record_model(self):
        """Test LogRecord model"""
        log = LogRecord.objects.create(
            level='INFO',
            message='Test log message',
            logger_name='test.logger',
            func_name='test_function',
            line_no=42,
            thread='MainThread',
            process='12345',
            request_id='test-request-123'
        )
        
        self.assertEqual(str(log), log.message)
        self.assertEqual(log.level, 'INFO')

    def test_log_record_serializer(self):
        """Test LogRecordSerializer"""
        log = LogRecord.objects.create(
            level='ERROR',
            message='Error occurred',
            logger_name='error.logger',
            func_name='error_func',
            line_no=100
        )
        
        serializer = LogRecordSerializer(instance=log)
        data = serializer.data
        
        self.assertEqual(data['level'], 'ERROR')
        self.assertEqual(data['message'], 'Error occurred')
        self.assertIn('created_at', data)

    @patch('system.views.LogRecord.objects.filter')
    def test_log_record_viewset_list(self, mock_filter):
        """Test LogRecordViewSet list method"""
        # Create mock logs
        mock_log1 = Mock(spec=LogRecord)
        mock_log1.level = 'INFO'
        mock_log1.message = 'Info log'
        
        mock_log2 = Mock(spec=LogRecord)
        mock_log2.level = 'ERROR'
        mock_log2.message = 'Error log'
        
        mock_queryset = Mock()
        mock_queryset.order_by.return_value = [mock_log1, mock_log2]
        mock_filter.return_value = mock_queryset
        
        request = self.factory.get('/api/logs/')
        request.user = self.user
        request.query_params = {}
        
        viewset = LogRecordViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()
        
        # Should call filter and order_by
        mock_filter.assert_called_once()


@pytest.mark.django_db
class TestMockModule(TestCase):
    """Test mock module"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='mockuser',
            email='mock@example.com',
            password=TEST_PASSWORD
        )
        
        self.project = Project.objects.create(
            name="Mock Test Project",
            desc="Test",
            responsible="mockuser"
        )
        
        self.mock_project = MockProject.objects.create(
            name="Mock Project 1",
            base_url="/mock/project1",
            description="Test mock project",
            faster_project=self.project
        )

    def test_mock_project_model(self):
        """Test MockProject model"""
        self.assertEqual(str(self.mock_project), "Mock Project 1")
        self.assertEqual(self.mock_project.base_url, "/mock/project1")

    def test_mock_api_model(self):
        """Test MockAPI model"""
        mock_api = MockAPI.objects.create(
            mock_project=self.mock_project,
            method="GET",
            path="/api/users",
            description="Get users",
            status_code=200,
            content_type="application/json",
            headers=json.dumps({"X-Custom": "value"}),
            response_body=json.dumps({"users": [{"id": 1, "name": "Test"}]}),
            is_active=True
        )
        
        self.assertEqual(str(mock_api), f"GET {self.mock_project.base_url}/api/users")
        self.assertTrue(mock_api.is_active)

    def test_mock_project_serializer(self):
        """Test MockProjectSerializer"""
        serializer = MockProjectSerializer(instance=self.mock_project)
        data = serializer.data
        
        self.assertEqual(data['name'], "Mock Project 1")
        self.assertEqual(data['base_url'], "/mock/project1")
        self.assertIn('id', data)

    def test_mock_api_serializer(self):
        """Test MockAPISerializer"""
        mock_api = MockAPI.objects.create(
            mock_project=self.mock_project,
            method="POST",
            path="/api/create",
            status_code=201,
            response_body=json.dumps({"id": 123})
        )
        
        serializer = MockAPISerializer(instance=mock_api)
        data = serializer.data
        
        self.assertEqual(data['method'], "POST")
        self.assertEqual(data['path'], "/api/create")
        self.assertEqual(data['status_code'], 201)

    @patch('mock.views.request_log', mock_request_log)
    def test_mock_project_view_list(self):
        """Test MockProjectView list method"""
        from mock.views import MockProjectView
        
        request = self.factory.get('/api/mock/project/')
        request.user = self.user
        request.query_params = {'faster_project': self.project.id}
        
        view = MockProjectView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)

    @patch('mock.views.request_log', mock_request_log)
    def test_mock_project_view_create(self):
        """Test MockProjectView create method"""
        from mock.views import MockProjectView
        
        request = self.factory.post('/api/mock/project/')
        request.user = self.user
        request.data = {
            'name': 'New Mock Project',
            'base_url': '/mock/new',
            'description': 'New test project',
            'faster_project': self.project.id
        }
        
        view = MockProjectView()
        response = view.create(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Mock Project')

    @patch('mock.views.request_log', mock_request_log)
    def test_mock_api_view_list(self):
        """Test MockAPIView list method"""
        from mock.views import MockAPIView
        
        # Create some mock APIs
        MockAPI.objects.create(
            mock_project=self.mock_project,
            method="GET",
            path="/api/test1",
            status_code=200,
            response_body='{"test": 1}'
        )
        
        request = self.factory.get('/api/mock/api/')
        request.user = self.user
        request.query_params = {'mock_project': self.mock_project.id}
        
        view = MockAPIView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)

    @patch('mock.views.request_log', mock_request_log)
    def test_mock_api_view_create(self):
        """Test MockAPIView create method"""
        from mock.views import MockAPIView
        
        request = self.factory.post('/api/mock/api/')
        request.user = self.user
        request.data = {
            'mock_project': self.mock_project.id,
            'method': 'POST',
            'path': '/api/new',
            'description': 'New API',
            'status_code': 201,
            'content_type': 'application/json',
            'response_body': '{"created": true}',
            'is_active': True
        }
        
        view = MockAPIView()
        response = view.create(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['method'], 'POST')

    def test_mock_response_view_get(self):
        """Test MockResponseView GET method"""
        # Create active mock API
        mock_api = MockAPI.objects.create(
            mock_project=self.mock_project,
            method="GET",
            path="/test",
            status_code=200,
            content_type="application/json",
            headers=json.dumps({"X-Test": "value"}),
            response_body=json.dumps({"success": True}),
            is_active=True
        )
        
        request = self.factory.get(f'{self.mock_project.base_url}/test')
        request.user = self.user
        
        view = MockResponseView()
        response = view.get(request, base_url=self.mock_project.base_url, path='test')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"success": True})
        self.assertEqual(response['X-Test'], 'value')

    def test_mock_response_view_post(self):
        """Test MockResponseView POST method"""
        mock_api = MockAPI.objects.create(
            mock_project=self.mock_project,
            method="POST",
            path="/create",
            status_code=201,
            response_body=json.dumps({"id": 123, "created": True}),
            is_active=True
        )
        
        request = self.factory.post(
            f'{self.mock_project.base_url}/create',
            data={"name": "test"},
            format='json'
        )
        request.user = self.user
        
        view = MockResponseView()
        response = view.post(request, base_url=self.mock_project.base_url, path='create')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["id"], 123)

    def test_mock_response_view_not_found(self):
        """Test MockResponseView when API not found"""
        request = self.factory.get(f'{self.mock_project.base_url}/nonexistent')
        request.user = self.user
        
        view = MockResponseView()
        response = view.get(request, base_url=self.mock_project.base_url, path='nonexistent')
        
        self.assertEqual(response.status_code, 404)

    def test_mock_response_view_inactive(self):
        """Test MockResponseView with inactive API"""
        mock_api = MockAPI.objects.create(
            mock_project=self.mock_project,
            method="GET",
            path="/inactive",
            status_code=200,
            response_body='{"test": true}',
            is_active=False
        )
        
        request = self.factory.get(f'{self.mock_project.base_url}/inactive')
        request.user = self.user
        
        view = MockResponseView()
        response = view.get(request, base_url=self.mock_project.base_url, path='inactive')
        
        self.assertEqual(response.status_code, 404)

    def test_get_req_json(self):
        """Test get_req_json function"""
        # Test with JSON body
        request = Mock()
        request.body = b'{"test": "data"}'
        
        result = get_req_json(request)
        self.assertEqual(result, {"test": "data"})
        
        # Test with empty body
        request.body = b''
        result = get_req_json(request)
        self.assertEqual(result, {})
        
        # Test with invalid JSON
        request.body = b'invalid json'
        result = get_req_json(request)
        self.assertEqual(result, {})

    def test_mock_response_all_methods(self):
        """Test MockResponseView for all HTTP methods"""
        methods = ['PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
        
        for method in methods:
            mock_api = MockAPI.objects.create(
                mock_project=self.mock_project,
                method=method,
                path=f"/{method.lower()}",
                status_code=200,
                response_body=json.dumps({"method": method}),
                is_active=True
            )
            
            request = getattr(self.factory, method.lower())(
                f'{self.mock_project.base_url}/{method.lower()}',
                data={"test": "data"} if method in ['PUT', 'PATCH'] else None,
                format='json' if method in ['PUT', 'PATCH'] else None
            )
            request.user = self.user
            
            view = MockResponseView()
            response = getattr(view, method.lower())(
                request, 
                base_url=self.mock_project.base_url, 
                path=method.lower()
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["method"], method)


@pytest.mark.django_db 
class TestMockTasks(TestCase):
    """Test mock.tasks module"""
    
    @patch('mock.models.MockAPI.objects.filter')
    def test_update_mock_api_update_time(self):
        """Test update_mock_api_update_time task"""
        from mock.tasks import update_mock_api_update_time
        
        # Create mock API objects
        mock_api1 = Mock()
        mock_api2 = Mock()
        
        mock_filter = Mock()
        mock_filter.update.return_value = 2
        MockAPI.objects.filter.return_value = mock_filter
        
        # Call the task
        update_mock_api_update_time()
        
        # Verify filter was called with is_active=True
        MockAPI.objects.filter.assert_called_once_with(is_active=True)
        
        # Verify update was called
        mock_filter.update.assert_called_once()
        update_call_args = mock_filter.update.call_args[1]
        self.assertIn('update_time', update_call_args)


@pytest.mark.django_db
class TestSystemTasks(TestCase):
    """Test system.tasks module"""
    
    @patch('system.models.LogRecord.objects.filter')
    def test_delete_logs(self):
        """Test delete_logs task"""
        from system.tasks import delete_logs
        
        # Mock old logs
        mock_filter = Mock()
        mock_filter.delete.return_value = (10, {'system.LogRecord': 10})
        LogRecord.objects.filter.return_value = mock_filter
        
        # Call the task
        delete_logs()
        
        # Verify filter was called
        LogRecord.objects.filter.assert_called_once()
        
        # Verify delete was called
        mock_filter.delete.assert_called_once()