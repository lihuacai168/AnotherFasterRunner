import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from fastrunner.models import (
    API, Case, CaseStep, Config, HostIP, Project, 
    Relation, Report, Variables
)
from fastrunner.utils import loader, parser, response as resp_utils
from fastrunner.utils.host import parse_host
from fastrunner.utils.parser import Format
from fastuser.models import MyUser, UserToken, UserInfo


@pytest.mark.integration
@pytest.mark.django_db
class TestUtilsIntegration(TestCase):
    """Integration tests for utility functions"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='utiluser',
            email='util@example.com',
            password='testpass123'
        )
        self.user_info = UserInfo.objects.create(
            username='utiluser',
            email='util@example.com',
            password='testpass123'
        )
        self.token = UserToken.objects.create(user=self.user_info, token='util-token-123')
        
        self.project = Project.objects.create(
            name="Utils Test Project",
            desc="Project for utils testing",
            responsible="utiluser"
        )

    def test_parser_format(self):
        """Test API format parser"""
        
        api_data = {
            "name": "Parser Test API",
            "project": self.project.id,
            "relation": 1,
            "method": "POST",
            "url": "/api/test",
            "header": {
                "header": {"Content-Type": "application/json"},
                "desc": {"Content-Type": "Content type header"}
            },
            "request": {
                "json": {"username": "test", "password": "pass"},
                "params": {
                    "params": {"page": 1},
                    "desc": {"page": "Page number"}
                }
            },
            "validate": {
                "validate": [
                    {"equals": ["status_code", 200]},
                    {"contains": ["content.message", "success"]}
                ]
            },
            "extract": {
                "extract": [{"token": "content.token"}],
                "desc": {"token": "Auth token"}
            }
        }
        
        formatter = Format(api_data)
        formatter.parse()
        
        self.assertEqual(formatter.name, "Parser Test API")
        self.assertEqual(formatter.method, "POST")
        self.assertEqual(formatter.url, "/api/test")
        self.assertIsInstance(formatter.testcase, dict)

    def test_host_parsing(self):
        """Test host URL parsing functionality"""
        
        test_case = {
            "request": {
                "url": "https://api.example.com/api/v1/users",
                "method": "GET",
                "headers": {"Authorization": "Bearer $token"}
            }
        }
        
        # Test with non-list parameter (should return original)
        host = "https://api.example.com"
        parsed = parse_host(host, test_case)
        self.assertEqual(parsed, test_case)  # Returns original when not a list
        
        # Test with empty host list
        host = []
        parsed = parse_host(host, test_case)
        self.assertEqual(parsed["request"]["url"], "https://api.example.com/api/v1/users")
        
        # Test with hosts list (simulating /etc/hosts entries)
        host = ["127.0.0.1 api.example.com", "# Comment line"]
        test_case_copy = test_case.copy()
        parsed = parse_host(host, test_case_copy)
        # Should replace hostname with IP address
        self.assertIn("127.0.0.1", parsed["request"]["url"])

    def test_response_utils(self):
        """Test response utility functions"""
        
        # Test success responses
        self.assertEqual(resp_utils.SYSTEM_ERROR['msg'], 'System Error')
        self.assertEqual(resp_utils.VALIDATE_ERROR['msg'], '参数校验错误')
        self.assertEqual(resp_utils.AUTH_FAIL['msg'], '请登录')
        
        # Test response codes
        self.assertEqual(resp_utils.SYSTEM_ERROR['code'], '9999')
        self.assertEqual(resp_utils.VALIDATE_ERROR['code'], '9998')


@pytest.mark.integration
@pytest.mark.django_db
class TestAPIWorkflowIntegration(TestCase):
    """Integration tests for complete API testing workflow"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='workflowuser',
            email='workflow@example.com',
            password='testpass123'
        )
        self.user_info = UserInfo.objects.create(
            username='workflowuser',
            email='workflow@example.com',
            password='testpass123'
        )
        self.token = UserToken.objects.create(user=self.user_info, token='workflow-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Workflow Test Project",
            desc="Project for workflow testing",
            responsible="workflowuser"
        )

    def test_api_with_variables_and_extraction(self):
        """Test API with variables and data extraction"""
        
        # Step 1: Create global variable
        global_var = Variables.objects.create(
            key="base_url",
            value="https://api.test.com",
            description="Base API URL",
            project=self.project
        )
        
        # Step 2: Create project variable
        project_var = Variables.objects.create(
            key="api_key",
            value="test-api-key-123",
            project=self.project,
            description="Project API key"
        )
        
        # Step 3: Create config using variables
        config_body = {
            "name": "Variable Test Config",
            "request": {
                "base_url": "$base_url",
                "headers": {
                    "X-API-Key": "$api_key"
                }
            },
            "variables": [
                {"timeout": 30}
            ]
        }
        
        config = Config.objects.create(
            name="Variable Test Config",
            project=self.project,
            body=json.dumps(config_body)
        )
        
        # Step 4: Create API that uses extraction
        api_body = {
            "name": "Login API",
            "request": {
                "url": "/api/auth/login",
                "method": "POST",
                "json": {
                    "username": "testuser",
                    "password": "testpass"
                }
            },
            "extract": [
                {"auth_token": "content.token"},
                {"user_id": "content.user.id"}
            ],
            "validate": [
                {"equals": ["status_code", 200]},
                {"type_match": ["content.token", "str"]}
            ]
        }
        
        api = API.objects.create(
            name="Login API",
            project=self.project,
            method="POST",
            url="/api/auth/login",
            body=json.dumps(api_body),
            relation=1
        )
        
        # Step 5: Create API that uses extracted data
        api2_body = {
            "name": "Get User Info",
            "request": {
                "url": "/api/users/$user_id",
                "method": "GET",
                "headers": {
                    "Authorization": "Bearer $auth_token"
                }
            },
            "validate": [
                {"equals": ["status_code", 200]},
                {"equals": ["content.id", "$user_id"]}
            ]
        }
        
        api2 = API.objects.create(
            name="Get User Info",
            project=self.project,
            method="GET",
            url="/api/users/$user_id",
            body=json.dumps(api2_body),
            relation=1
        )
        
        # Step 6: Create test case with both APIs
        case = Case.objects.create(
            name="Login and Get User Info",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=2     # Required API count
        )
        
        # Add steps
        CaseStep.objects.create(
            case=case,
            name="Login",
            step=1,
            source_api_id=api.id,
            body=api.body,
            url=api.url,
            method=api.method
        )
        
        CaseStep.objects.create(
            case=case,
            name="Get User Info",
            step=2,
            source_api_id=api2.id,
            body=api2.body,
            url=api2.url,
            method=api2.method
        )
        
        # Verify the setup
        self.assertEqual(CaseStep.objects.filter(case=case).count(), 2)
        self.assertEqual(Variables.objects.filter(project=self.project).count(), 2)  # Both variables belong to project

    def test_api_with_setup_and_teardown_hooks(self):
        """Test API with setup and teardown hooks"""
        
        api_body = {
            "name": "API with Hooks",
            "request": {
                "url": "/api/data",
                "method": "GET"
            },
            "hooks": {
                "setup_hooks": [
                    "${setup_database()}",
                    "${generate_test_data()}"
                ],
                "teardown_hooks": [
                    "${cleanup_test_data()}",
                    "${reset_database()}"
                ]
            },
            "validate": [
                {"equals": ["status_code", 200]}
            ]
        }
        
        api = API.objects.create(
            name="API with Hooks",
            project=self.project,
            method="GET",
            url="/api/data",
            body=json.dumps(api_body),
            relation=1
        )
        
        # Verify hooks are stored correctly
        body = json.loads(api.body)
        self.assertIn('hooks', body)
        self.assertEqual(len(body['hooks']['setup_hooks']), 2)
        self.assertEqual(len(body['hooks']['teardown_hooks']), 2)

    def test_api_with_file_upload(self):
        """Test API with file upload"""
        
        api_body = {
            "name": "File Upload API",
            "request": {
                "url": "/api/upload",
                "method": "POST",
                "files": {
                    "files": {
                        "document": "test.pdf",
                        "image": "photo.jpg"
                    },
                    "desc": {
                        "document": "PDF document",
                        "image": "User photo"
                    }
                },
                "form": {
                    "data": {
                        "title": "Test Upload",
                        "description": "Test file upload"
                    },
                    "desc": {
                        "title": "Upload title",
                        "description": "Upload description"
                    }
                }
            },
            "validate": [
                {"equals": ["status_code", 201]},
                {"contains": ["content.message", "uploaded successfully"]}
            ]
        }
        
        api = API.objects.create(
            name="File Upload API",
            project=self.project,
            method="POST",
            url="/api/upload",
            body=json.dumps(api_body),
            relation=1  # Required field for node id
        )
        
        # Verify file upload configuration
        body = json.loads(api.body)
        self.assertIn('files', body['request'])
        self.assertIn('form', body['request'])
        self.assertEqual(len(body['request']['files']['files']), 2)


@pytest.mark.integration
@pytest.mark.django_db
class TestErrorHandling(TestCase):
    """Integration tests for error handling"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='erroruser',
            email='error@example.com',
            password='testpass123'
        )
        
        # Use JWT authentication as that's what the app actually uses
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_invalid_project_access(self):
        """Test accessing non-existent project"""
        
        response = self.client.get('/api/fastrunner/project/99999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], '0001')
        
    def test_invalid_api_data(self):
        """Test creating API with invalid data"""
        
        # Missing required fields
        invalid_data = {
            "name": "Invalid API"
            # Missing project, url, method
        }
        
        response = self.client.post('/api/fastrunner/api/', invalid_data, format='json')
        # Should return validation error
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_unauthorized_access(self):
        """Test accessing API without authentication"""
        
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get('/api/fastrunner/project/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.integration
@pytest.mark.django_db
class TestCIIntegration(TestCase):
    """Integration tests for CI/CD integration"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='ciuser',
            email='ci@example.com',
            password='testpass123'
        )
        self.user_info = UserInfo.objects.create(
            username='ciuser',
            email='ci@example.com',
            password='testpass123'
        )
        self.token = UserToken.objects.create(user=self.user_info, token='ci-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="CI Test Project",
            desc="Project for CI testing",
            responsible="ciuser"
        )

    @patch('fastrunner.views.ci.prepare_suite_kwargs')
    @patch('fastrunner.views.ci.debug_suite')
    def test_gitlab_ci_integration(self, mock_debug_suite, mock_prepare_kwargs):
        """Test GitLab CI integration"""
        
        # Create test suite
        case = Case.objects.create(
            name="CI Test Case",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        
        mock_prepare_kwargs.return_value = ({}, {"config": {}})
        mock_debug_suite.return_value = {
            "success": True,
            "report_id": 123
        }
        
        ci_data = {
            "project": self.project.id,
            "cases": [case.id],
            "config": "",
            "run_type": "deploy"
        }
        
        response = self.client.post('/api/fastrunner/gitlab-ci/', ci_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get CI report URL
        response = self.client.get('/api/fastrunner/gitlab-ci/', {'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)