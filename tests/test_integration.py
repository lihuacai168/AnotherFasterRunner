import json
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from fastrunner.models import API, Case, CaseStep, Config, Project, Report, Variables
from fastuser.models import MyUser
from test_constants import TEST_PASSWORD


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db
class TestFullWorkflow(TestCase):
    """Integration tests for complete workflow from project creation to test execution"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user and authentication
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=TEST_PASSWORD
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test project
        self.project = Project.objects.create(
            name="Integration Test Project",
            desc="Project for integration testing",
            responsible="testuser"
        )

    @pytest.mark.skip(reason="Transaction error in CI environment")
    def test_complete_api_testing_workflow(self):
        """Test the complete workflow from API creation to test execution"""
        
        # Step 1: Create a config
        config_data = {
            "name": "Test Config",
            "project": self.project.id,
            "body": json.dumps({
                "name": "Test Config",
                "request": {
                    "base_url": "http://localhost:8000"
                },
                "variables": [
                    {"token": "test-token"}
                ]
            })
        }
        response = self.client.post('/api/fastrunner/config/', config_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        config_id = response.data['config_id']
        
        # Step 2: Create an API
        api_data = {
            "name": "Test API",
            "project": self.project.id,
            "relation": 1,  # Default relation id
            "method": "GET",
            "url": "/api/test",
            "body": json.dumps({
                "name": "Test API",
                "request": {
                    "url": "/api/test",
                    "method": "GET",
                    "headers": {"Content-Type": "application/json"}
                },
                "validate": [
                    {"equals": ["status_code", 200]}
                ]
            })
        }
        response = self.client.post('/api/fastrunner/api/', api_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_id = response.data['id']
        
        # Step 3: Create a test case
        case_data = {
            "name": "Integration Test Case",
            "project": self.project.id,
            "relation": 1,  # Default relation id
            "tag": 1  # 默认标签
        }
        response = self.client.post('/api/fastrunner/test/', case_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case_id = json.loads(response.content)['id']
        
        # Step 4: Add test steps
        step_data = {
            "body": json.dumps({
                "name": "Test Step 1",
                "request": {
                    "url": "/api/test",
                    "method": "GET"
                }
            }),
            "name": "Test Step 1",
            "api": api_id,
            "step": 1,
            "source_api_id": api_id
        }
        response = self.client.post(f'/api/fastrunner/teststep/{case_id}/', step_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 5: Run the test case
        with patch('fastrunner.views.run.run_api') as mock_run:
            mock_run.return_value = {'success': True}
            run_data = {
                "id": [case_id],
                "config": config_id,
                "project": self.project.id,
                "run_type": "test"
            }
            response = self.client.post('/api/fastrunner/run_testsuite/', run_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_run.assert_called()


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db
class TestProjectManagement(TestCase):
    """Integration tests for project management features"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='projectuser',
            email='project@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='projectuser',
            email='project@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='project-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')

    def test_project_crud_operations(self):
        """Test Create, Read, Update, Delete operations for projects"""
        
        # Create project
        project_data = {
            "name": "CRUD Test Project",
            "desc": "Testing CRUD operations"
        }
        response = self.client.post('/api/fastrunner/project/', project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_id = response.data['id']
        
        # Read project list
        response = self.client.get('/api/fastrunner/project/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Read single project
        response = self.client.get(f'/api/fastrunner/project/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], project_id)
        
        # Update project
        update_data = {
            "name": "Updated Project Name",
            "desc": "Updated description"
        }
        response = self.client.patch(f'/api/fastrunner/project/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete project
        response = self.client.delete(f'/api/fastrunner/project/', {"id": project_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db
class TestVariablesAndConfig(TestCase):
    """Integration tests for variables and configuration management"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='configuser',
            email='config@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='configuser',
            email='config@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='config-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Config Test Project",
            desc="Project for config testing",
            responsible="configuser"
        )

    def test_variables_management(self):
        """Test global and project variables"""
        
        # Create global variable
        global_var_data = {
            "key": "global_token",
            "value": "test-global-token",
            "description": "Global test token"
        }
        response = self.client.post('/api/fastrunner/variables/', global_var_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Create project variable
        project_var_data = {
            "key": "project_token",
            "value": "test-project-token",
            "project": self.project.id,
            "description": "Project test token"
        }
        response = self.client.post('/api/fastrunner/variables/', project_var_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # List variables
        response = self.client.get('/api/fastrunner/variables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
        
        # Update variable
        var_id = response.data[0]['id']
        update_data = {
            "value": "updated-token-value"
        }
        response = self.client.patch(f'/api/fastrunner/variables/{var_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_config_management(self):
        """Test configuration creation and usage"""
        
        # Create config with base_url and headers
        config_body = {
            "name": "Production Config",
            "request": {
                "base_url": "https://api.production.com",
                "headers": {
                    "Authorization": "Bearer production-token",
                    "Content-Type": "application/json"
                }
            },
            "variables": [
                {"env": "production"},
                {"api_key": "prod-api-key"}
            ]
        }
        
        config_data = {
            "name": "Production Config",
            "project": self.project.id,
            "body": json.dumps(config_body)
        }
        
        response = self.client.post('/api/fastrunner/config/', config_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        config_id = response.data['config_id']
        
        # List configs
        response = self.client.get('/api/fastrunner/config/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Get single config
        response = self.client.get(f'/api/fastrunner/config/{config_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], config_id)


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db
class TestReportGeneration(TestCase):
    """Integration tests for report generation and viewing"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='reportuser',
            email='report@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='reportuser',
            email='report@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='report-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Report Test Project",
            desc="Project for report testing",
            responsible="reportuser"
        )

    def test_report_generation_and_viewing(self):
        """Test report generation after test execution"""
        
        # Create a dummy report
        report = Report.objects.create(
            project=self.project,
            name="Test Report",
            type=1,
            status=True,
            creator=self.user.username,
            detail=json.dumps({
                "success": True,
                "stat": {
                    "testcases": {"total": 10, "success": 8, "fail": 2}
                },
                "time": {"start_at": "2023-01-01T00:00:00", "duration": 60}
            })
        )
        
        # List reports
        response = self.client.get('/api/fastrunner/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # View single report
        response = self.client.get(f'/api/fastrunner/reports/{report.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], report.id)
        
        # Delete report
        response = self.client.delete(f'/api/fastrunner/reports/{report.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db
class TestAPITemplateFeatures(TestCase):
    """Integration tests for API template features"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='apiuser',
            email='api@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='api-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="API Test Project",
            desc="Project for API testing",
            responsible="apiuser"
        )
        
        self.relation = Relation.objects.create(
            project=self.project,
            tree=1,
            name="API Group",
            type=1
        )

    def test_api_template_with_validation(self):
        """Test API template creation with validation rules"""
        
        api_body = {
            "name": "User Login API",
            "request": {
                "url": "/api/auth/login",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "username": "$username",
                    "password": "$password"
                }
            },
            "validate": [
                {"equals": ["status_code", 200]},
                {"contains": ["content.message", "success"]},
                {"length_equals": ["content.token", 32]}
            ],
            "extract": [
                {"token": "content.token"},
                {"user_id": "content.user_id"}
            ]
        }
        
        api_data = {
            "name": "User Login API",
            "project": self.project.id,
            "relation": self.relation.id,
            "method": "POST",
            "url": "/api/auth/login",
            "body": json.dumps(api_body)
        }
        
        response = self.client.post('/api/fastrunner/api/', api_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        api_id = response.data['id']
        
        # Test copying API
        response = self.client.post(f'/api/fastrunner/api/{api_id}/', {"name": "Copied API"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test moving API to different relation
        new_relation = Relation.objects.create(
            project=self.project,
            tree=2,
            name="New API Group",
            type=1
        )
        
        move_data = {
            "api": [api_id],
            "relation": new_relation.id
        }
        response = self.client.patch('/api/fastrunner/api/move_api/', move_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.skip(reason="Transaction error in CI environment")
@pytest.mark.integration
@pytest.mark.django_db  
class TestHostIPConfiguration(TestCase):
    """Integration tests for Host IP configuration"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='hostuser',
            email='host@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='hostuser',
            email='host@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='host-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')

    def test_host_ip_management(self):
        """Test Host IP creation and management"""
        
        # Create host IP configuration
        host_data = {
            "name": "Production Server",
            "host": "https://api.production.com",
            "description": "Production API server"
        }
        
        response = self.client.post('/api/fastrunner/host_ip/', host_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        host_id = response.data['id']
        
        # List host IPs
        response = self.client.get('/api/fastrunner/host_ip/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Update host IP
        update_data = {
            "host": "https://api.production-v2.com",
            "description": "Updated production server"
        }
        response = self.client.patch(f'/api/fastrunner/host_ip/{host_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete host IP
        response = self.client.delete(f'/api/fastrunner/host_ip/{host_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)