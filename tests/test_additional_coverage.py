import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from fastrunner.models import Project
from fastrunner.utils import response as resp_utils
from fastrunner.utils.parser import Format
from fastuser.models import MyUser, UserToken, UserInfo
from fastuser.common import response as user_resp


@pytest.mark.django_db
class TestFastUserViews(TestCase):
    """Test fastuser views"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    @pytest.mark.skip(reason="Registration endpoint is disabled")
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/api/user/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], '注册成功')

    def test_user_login(self):
        """Test user login"""
        # First create user
        MyUser.objects.create_user(**self.user_data)
        
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/user/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    @pytest.mark.skip(reason="Registration endpoint is disabled")
    def test_duplicate_registration(self):
        """Test duplicate username registration"""
        # Create user first
        MyUser.objects.create_user(**self.user_data)
        
        # Try to register with same username
        response = self.client.post('/api/user/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], '0001')
        self.assertIn('用户名已被注册', response.data['msg'])

    def test_login_with_wrong_password(self):
        """Test login with wrong password"""
        MyUser.objects.create_user(**self.user_data)
        
        login_data = {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/user/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], '0103')  # LOGIN_FAILED code

    @pytest.mark.skip(reason="User info endpoint does not exist")
    def test_get_user_info(self):
        """Test getting user info with authentication"""
        # Create UserInfo for the token system
        user_info = UserInfo.objects.create(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='hashed_password'  # This would normally be hashed
        )
        token = UserToken.objects.create(user=user_info, token='test-token-123')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')
        response = self.client.get('/api/user/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])

    @pytest.mark.skip(reason="User info endpoint does not exist") 
    def test_get_user_info_without_auth(self):
        """Test getting user info without authentication"""
        response = self.client.get('/api/user/info/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.skip(reason="Logout endpoint does not exist")
    def test_logout(self):
        """Test user logout"""
        # Create UserInfo for the token system
        user_info = UserInfo.objects.create(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='hashed_password'
        )
        token = UserToken.objects.create(user=user_info, token='test-token-123')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')
        response = self.client.get('/api/user/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token is deleted
        self.assertFalse(UserToken.objects.filter(token=token.token).exists())


@pytest.mark.django_db
class TestFastUserCommon(TestCase):
    """Test fastuser common response constants"""

    def test_response_constants(self):
        """Test response constants"""
        self.assertEqual(user_resp.KEY_MISS['code'], '0100')
        self.assertEqual(user_resp.KEY_MISS['success'], False)
        
        self.assertEqual(user_resp.REGISTER_USERNAME_EXIST['code'], '0101')
        self.assertEqual(user_resp.LOGIN_FAILED['code'], '0103')
        self.assertEqual(user_resp.USER_NOT_EXISTS['code'], '0104')
        
        self.assertEqual(user_resp.REGISTER_SUCCESS['success'], True)
        self.assertEqual(user_resp.LOGIN_SUCCESS['success'], True)


@pytest.mark.django_db
class TestMockViews(TestCase):
    """Test mock views"""

    def setUp(self):
        self.client = APIClient()
        # Create MyUser for JWT authentication (which is what the app actually uses)
        self.user = MyUser.objects.create_user(
            username='mockuser',
            email='mock@example.com',
            password='testpass123'
        )
        
        # Use JWT authentication as that's what the app actually uses
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        
        self.client.credentials(HTTP_AUTHORIZATION=token)
        
        self.project = Project.objects.create(
            name="Mock Test Project",
            desc="Project for mock testing",
            responsible="mockuser"
        )

    def test_create_mock_project(self):
        """Test creating a mock project"""
        data = {
            'project_name': 'Mock Project',
            'project_desc': 'Test mock project',
            'is_active': True
        }
        response = self.client.post('/api/mock/mock_project/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['project_name'], 'Mock Project')

    def test_list_mock_projects(self):
        """Test listing mock projects"""
        response = self.client.get('/api/mock/mock_project/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

    def test_create_mock_api(self):
        """Test creating a mock API"""
        # First create a mock project
        project_data = {
            'project_name': 'Mock Project for API',
            'project_desc': 'Test project',
            'is_active': True
        }
        project_resp = self.client.post('/api/mock/mock_project/', project_data, format='json')
        project_id = project_resp.data['id']
        
        # Create mock API
        api_data = {
            'project': project_id,
            'method': 'GET',
            'url': '/api/test',
            'response_data': json.dumps({'message': 'Hello World'}),
            'status_code': 200,
            'description': 'Test API'
        }
        response = self.client.post('/api/mock/mock_api/', api_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['method'], 'GET')
        self.assertEqual(response.data['url'], '/api/test')


@pytest.mark.django_db
class TestSystemViews(TestCase):
    """Test system views"""

    def setUp(self):
        self.client = APIClient()
        # Create MyUser for JWT authentication (which is what the app actually uses)
        self.user = MyUser.objects.create_user(
            username='systemuser',
            email='system@example.com',
            password='testpass123'
        )
        
        # Use JWT authentication as that's what the app actually uses
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_log_records_list(self):
        """Test listing log records"""
        response = self.client.get('/api/system/log_records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

    def test_log_records_pagination(self):
        """Test log records pagination"""
        response = self.client.get('/api/system/log_records/', {'page': 1, 'page_size': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)


@pytest.mark.django_db
class TestUtilsAndHelpers(TestCase):
    """Test utility functions and helpers"""

    def test_response_constants(self):
        """Test response utility constants"""
        self.assertEqual(resp_utils.SYSTEM_ERROR['code'], '9999')
        self.assertEqual(resp_utils.VALIDATE_ERROR['code'], '9998')
        self.assertEqual(resp_utils.AUTH_FAIL['code'], '9997')
        self.assertEqual(resp_utils.TASK_NOT_EXIST['code'], '0005')
        
        self.assertEqual(resp_utils.PROJECT_ADD_SUCCESS['msg'], '项目创建成功')
        self.assertEqual(resp_utils.API_ADD_SUCCESS['msg'], '接口创建成功')
        self.assertEqual(resp_utils.CASE_ADD_SUCCESS['msg'], '用例添加成功')

    def test_parser_format_basic(self):
        """Test basic parser format functionality"""
        api_data = {
            'name': 'Test API',
            'project': 1,
            'method': 'GET',
            'url': '/api/test',
            'header': {
                'header': {'Content-Type': 'application/json'},
                'desc': {}
            },
            'request': {
                'json': {},
                'params': {
                    'params': {},
                    'desc': {}
                }
            }
        }
        
        formatter = Format(api_data, level='test')
        self.assertEqual(formatter.name, 'Test API')
        self.assertEqual(formatter.method, 'GET')
        self.assertEqual(formatter.url, '/api/test')

    def test_parser_format_with_extract_validate(self):
        """Test parser format with extract and validate"""
        api_data = {
            'name': 'Complex API',
            'project': 1,
            'method': 'POST',
            'url': '/api/complex',
            'extract': {
                'extract': [{'token': 'content.token'}],
                'desc': {}
            },
            'validate': {
                'validate': [{'equals': ['status_code', 200]}]
            },
            'request': {
                'json': {'username': 'test'},
                'params': {
                    'params': {},
                    'desc': {}
                }
            }
        }
        
        formatter = Format(api_data)
        formatter.parse()
        self.assertIsInstance(formatter.testcase, dict)
        self.assertIn('extract', formatter.testcase)
        self.assertIn('validate', formatter.testcase)


@pytest.mark.django_db  
class TestModelStr(TestCase):
    """Test model string representations"""

    def test_project_str(self):
        """Test Project model string representation"""
        project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        self.assertEqual(str(project), "Test Project")

    def test_user_str(self):
        """Test MyUser model string representation"""
        user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')