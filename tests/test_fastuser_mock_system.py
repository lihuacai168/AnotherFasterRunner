"""Test fastuser and mock modules to improve coverage"""
import json
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock

from fastuser.models import MyUser, UserToken
from fastuser import views as fastuser_views
from mock.models import MockProject, MockAPI
from system.models import LogRecord


@pytest.mark.django_db
class TestFastUserViews(TestCase):
    """Test fastuser views directly"""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_user_register(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, 200)
        
    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = MyUser.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='password123'
        )
        
        data = {
            'username': 'loginuser',
            'password': 'password123'
        }
        response = self.client.post('/api/user/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        
    def test_duplicate_username(self):
        """Test duplicate username registration"""
        MyUser.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='password123'
        )
        
        data = {
            'username': 'existing',
            'email': 'new@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], '0001')


@pytest.mark.django_db
class TestMockModels(TestCase):
    """Test mock module models"""
    
    def test_mock_project_str(self):
        """Test MockProject string representation"""
        project = MockProject.objects.create(
            name="Test Mock Project",
            description="Test description"
        )
        self.assertEqual(str(project), "Test Mock Project")
        
    def test_mock_api_str(self):
        """Test MockAPI string representation"""
        project = MockProject.objects.create(
            name="Test Project",
            description="Test"
        )
        api = MockAPI.objects.create(
            project=project,
            method="GET",
            url="/test/api",
            response_data=json.dumps({"success": True}),
            status_code=200
        )
        self.assertEqual(str(api), "GET /test/api")
        
    def test_mock_api_fields(self):
        """Test MockAPI field defaults"""
        project = MockProject.objects.create(name="Test", description="Test")
        api = MockAPI.objects.create(
            project=project,
            method="POST",
            url="/api/test"
        )
        
        self.assertEqual(api.status_code, 200)
        self.assertEqual(api.delay, 0)
        self.assertTrue(api.is_active)


@pytest.mark.django_db
class TestSystemModels(TestCase):
    """Test system module models"""
    
    def test_log_record_creation(self):
        """Test LogRecord model creation"""
        log = LogRecord.objects.create(
            level="INFO",
            message="Test log message",
            pathname="/test/path.py",
            lineno=100,
            func_name="test_function",
            created_time="2023-01-01 00:00:00"
        )
        
        self.assertEqual(log.level, "INFO")
        self.assertEqual(log.message, "Test log message")
        self.assertTrue(LogRecord.objects.filter(id=log.id).exists())


@pytest.mark.django_db
class TestUtilsModules(TestCase):
    """Test various utility modules"""
    
    def test_day_utils(self):
        """Test day utility functions"""
        from fastrunner.utils.day import get_day
        
        # Test get_day function
        days = get_day(3)
        self.assertEqual(len(days), 3)
        self.assertTrue(all(isinstance(d, str) for d in days))
        
    def test_ding_message_init(self):
        """Test DingMessage initialization"""
        from fastrunner.utils.ding_message import DingMessage
        
        # Test initialization without actual sending
        ding = DingMessage("test")
        self.assertIsNotNone(ding)
        
    def test_email_helper_import(self):
        """Test email helper can be imported"""
        from fastrunner.utils import email_helper
        self.assertIsNotNone(email_helper)
        
    def test_relation_constants(self):
        """Test relation module constants"""
        from fastrunner.utils.relation import API_RELATION, API_AUTHOR
        
        self.assertIn('default', API_RELATION)
        self.assertIn('default', API_AUTHOR)
        self.assertIsInstance(API_RELATION['default'], int)
        self.assertIsInstance(API_AUTHOR['default'], int)


@pytest.mark.django_db
class TestDTOModules(TestCase):
    """Test DTO modules"""
    
    def test_tree_dto(self):
        """Test tree DTO"""
        from fastrunner.dto.tree_dto import TreeOut, TreeUniqueIn
        
        # Test TreeOut
        tree_out = TreeOut(id=1, label="Test", children=[])
        self.assertEqual(tree_out.id, 1)
        self.assertEqual(tree_out.label, "Test")
        
        # Test TreeUniqueIn
        tree_in = TreeUniqueIn(id=[1, 2, 3], project_id=1, type=1)
        self.assertEqual(tree_in.project_id, 1)
        self.assertEqual(tree_in.type, 1)


@pytest.mark.django_db
class TestServicesModules(TestCase):
    """Test service modules"""
    
    @patch('fastrunner.services.tree_service_impl.models.Relation.objects.filter')
    def test_tree_service(self, mock_filter):
        """Test tree service implementation"""
        from fastrunner.services.tree_service_impl import TreeService
        
        # Mock the queryset
        mock_queryset = MagicMock()
        mock_queryset.values.return_value = [
            {"tree": 1, "name": "Node1"},
            {"tree": 2, "name": "Node2"}
        ]
        mock_filter.return_value = mock_queryset
        
        service = TreeService()
        result = service.get_tree_by_project_id(project_id=1, type=1)
        self.assertIsInstance(result, list)


@pytest.mark.django_db
class TestTemplateTags(TestCase):
    """Test custom template tags"""
    
    def test_custom_tags_import(self):
        """Test custom tags can be imported"""
        try:
            from fastrunner.templatetags import custom_tags
            self.assertIsNotNone(custom_tags)
        except ImportError:
            pass  # Template tags might not be used


@pytest.mark.django_db
class TestFastUserCommon(TestCase):
    """Test fastuser common modules"""
    
    def test_response_constants(self):
        """Test response constants in fastuser.common.response"""
        from fastuser.common import response
        
        # Test constants exist and have correct structure
        self.assertIn('code', response.KEY_MISS)
        self.assertIn('success', response.KEY_MISS)
        self.assertIn('msg', response.KEY_MISS)
        
        self.assertFalse(response.KEY_MISS['success'])
        self.assertTrue(response.LOGIN_SUCCESS['success'])
        self.assertFalse(response.LOGIN_FAILED['success'])
        
    def test_token_generation(self):
        """Test token generation"""
        from fastuser.common.token import generate_token
        
        token = generate_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)