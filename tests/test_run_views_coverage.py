"""Test for fastrunner.views.run module to improve coverage"""
import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from test_constants import TEST_PASSWORD

from fastrunner.models import API, Case, CaseStep, Config, HostIP, Project
from fastrunner.views.run import (
    run_api_pk,
    run_api_tree,
    run_testsuite,
    run_test,
    run_testsuite_pk,
    run_suite_tree,
    run_batch_test,
    get_project_id,
)
from fastuser.models import MyUser


def mock_request_log(func):
    """Mock request_log decorator"""
    return func


@pytest.mark.django_db
class TestRunViewsCoverage(TestCase):
    """Test run views to improve coverage"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='runuser',
            email='run@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Run Coverage Project",
            desc="Test",
            responsible="runuser"
        )
        
        self.config = Config.objects.create(
            name="Coverage Config",
            project=self.project,
            body=json.dumps({
                "name": "Coverage Config",
                "request": {
                    "base_url": "http://localhost:8000"
                }
            })
        )
        
        self.host = HostIP.objects.create(
            name="Test Host",
            host="http://testhost:8000",
            description="Test host"
        )
        
        self.api = API.objects.create(
            name="Coverage API",
            project=self.project,
            method="POST",
            url="/api/coverage",
            body=json.dumps({
                "name": "Coverage API",
                "request": {
                    "url": "/api/coverage",
                    "method": "POST",
                    "json": {"test": "data"}
                },
                "validate": [
                    {"eq": ["status_code", 200]}
                ]
            }),
            relation=1
        )
        
        self.case = Case.objects.create(
            name="Coverage Case",
            project=self.project,
            tag=2,  # 集合tag
            relation=1,
            length=2
        )
        
        self.case_step1 = CaseStep.objects.create(
            case=self.case,
            name="Config Step",
            step=1,
            body=json.dumps({
                "name": "Coverage Config",
                "request": {
                    "base_url": "http://localhost:8000"
                }
            }),
            url="",
            method="CONFIG"
        )
        
        self.case_step2 = CaseStep.objects.create(
            case=self.case,
            name="API Step",
            step=2,
            source_api_id=self.api.id,
            body=self.api.body,
            url=self.api.url,
            method=self.api.method
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_api')
    def test_run_api_pk_with_host(self, mock_debug):
        """Test run_api_pk with host parameter"""
        mock_debug.return_value = {
            "success": True,
            "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
        }
        
        request = self.factory.get(f'/api/run_api_pk/{self.api.id}/')
        request.user = self.user
        request.query_params = {
            'config': self.config.name,
            'project': self.project.id,
            'host': 'http://customhost:9000'
        }
        
        response = run_api_pk(request, pk=self.api.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        
        # Verify debug_api was called with correct params
        mock_debug.assert_called_once()
        call_args = mock_debug.call_args
        self.assertEqual(call_args[1]['host'], 'http://customhost:9000')

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_api')
    def test_run_api_tree_batch(self, mock_debug):
        """Test run_api_tree with multiple APIs"""
        mock_debug.return_value = {
            "success": True,
            "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
        }
        
        # Create another API
        api2 = API.objects.create(
            name="Coverage API 2",
            project=self.project,
            method="GET",
            url="/api/coverage2",
            body=json.dumps({
                "name": "Coverage API 2",
                "request": {"url": "/api/coverage2", "method": "GET"}
            }),
            relation=1
        )
        
        request = self.factory.post('/api/run_api_tree/')
        request.user = self.user
        request.data = {
            'id': [self.api.id, api2.id],
            'config': self.config.name,
            'project': self.project.id,
            'host': self.host.name,
            'run_type': 'api'
        }
        
        response = run_api_tree(request)
        
        self.assertEqual(response.status_code, 200)
        # Should be called twice (once for each API)
        self.assertEqual(mock_debug.call_count, 2)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_run_testsuite(self, mock_debug_suite):
        """Test run_testsuite function"""
        mock_debug_suite.return_value = (
            {
                "success": True,
                "stat": {"testcases": {"total": 2, "success": 2, "fail": 0}}
            },
            None
        )
        
        request = self.factory.post('/api/run_testsuite/')
        request.user = self.user
        request.data = {
            'id': [self.case.id],
            'config': self.config.name,
            'project': self.project.id,
            'host': 'Test Host',
            'run_type': 'suite'
        }
        
        response = run_testsuite(request)
        
        self.assertEqual(response.status_code, 200)
        mock_debug_suite.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_run_test(self, mock_debug_suite):
        """Test run_test function"""
        mock_debug_suite.return_value = (
            {
                "success": True,
                "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
            },
            None
        )
        
        request = self.factory.post('/api/run_test/')
        request.user = self.user
        request.data = {
            'id': [self.case.id],
            'config': self.config.name,
            'project': self.project.id,
            'run_type': 'test'
        }
        
        response = run_test(request)
        
        self.assertEqual(response.status_code, 200)
        mock_debug_suite.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_run_testsuite_pk(self, mock_debug_suite):
        """Test run_testsuite_pk function"""
        mock_debug_suite.return_value = (
            {
                "success": True,
                "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
            },
            None
        )
        
        request = self.factory.get(f'/api/run_testsuite_pk/{self.case.id}/')
        request.user = self.user
        request.query_params = {
            'config': self.config.name,
            'project': self.project.id
        }
        
        response = run_testsuite_pk(request, pk=self.case.id)
        
        self.assertEqual(response.status_code, 200)
        mock_debug_suite.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_run_suite_tree(self, mock_debug_suite):
        """Test run_suite_tree function"""
        mock_debug_suite.return_value = (
            {
                "success": True,
                "stat": {"testcases": {"total": 2, "success": 2, "fail": 0}}
            },
            None
        )
        
        request = self.factory.post('/api/run_suite_tree/')
        request.user = self.user
        request.data = {
            'id': [self.case.id],
            'config': self.config.name,
            'project': self.project.id,
            'run_type': 'suite'
        }
        
        response = run_suite_tree(request)
        
        self.assertEqual(response.status_code, 200)
        mock_debug_suite.assert_called_once()

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)  
    @patch('fastrunner.models.CaseStep.objects.filter')
    def test_run_batch_test(self, mock_filter):
        """Test run_batch_test function"""
        # Mock case steps
        mock_filter.return_value.order_by.return_value.values.return_value = [
            {"body": self.case_step1.body},
            {"body": self.case_step2.body}
        ]
        
        request = self.factory.post('/api/run_batch_test/')
        request.user = self.user
        request.data = {
            'id': json.dumps([self.case.id]),
            'config': self.config.name,
            'project': self.project.id,
            'type': 'case'
        }
        
        with patch('fastrunner.utils.loader.debug_api') as mock_debug:
            mock_debug.return_value = {
                "success": True,
                "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
            }
            
            response = run_batch_test(request)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('summary', response.data)

    def test_get_project_id(self):
        """Test get_project_id function"""
        # Test with Case
        result = get_project_id("Case", self.case.id)
        self.assertEqual(result, self.project.id)
        
        # Test with API
        result = get_project_id("API", self.api.id)
        self.assertEqual(result, self.project.id)
        
        # Test with invalid type
        result = get_project_id("Invalid", 999)
        self.assertIsNone(result)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_api')
    def test_run_api_pk_no_config(self, mock_debug):
        """Test run_api_pk without config"""
        mock_debug.return_value = {
            "success": True,
            "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
        }
        
        request = self.factory.get(f'/api/run_api_pk/{self.api.id}/')
        request.user = self.user
        request.query_params = {
            'config': '请选择',  # Special value meaning no config
            'project': self.project.id
        }
        
        response = run_api_pk(request, pk=self.api.id)
        
        self.assertEqual(response.status_code, 200)
        # Verify debug_api was called with config=None
        call_args = mock_debug.call_args
        self.assertIsNone(call_args[1]['config'])

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    @patch('fastrunner.utils.loader.debug_suite')
    def test_run_test_with_failure(self, mock_debug_suite):
        """Test run_test with test failures"""
        mock_debug_suite.return_value = (
            {
                "success": False,
                "stat": {"testcases": {"total": 2, "success": 1, "fail": 1}},
                "details": [
                    {"name": "test1", "success": True},
                    {"name": "test2", "success": False, "error": "AssertionError"}
                ]
            },
            None
        )
        
        request = self.factory.post('/api/run_test/')
        request.user = self.user
        request.data = {
            'id': [self.case.id],
            'config': self.config.name,
            'project': self.project.id,
            'run_type': 'test'
        }
        
        response = run_test(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['stat']['testcases']['fail'], 1)