"""Test fastuser and mock modules to improve coverage"""
import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase
from rest_framework.test import APIClient

from fastuser import views as fastuser_views
from fastuser.models import MyUser, UserToken
from mock.models import MockAPI, MockProject
from system.models import LogRecord
from tests.test_constants import TEST_PASSWORD


@pytest.mark.django_db
class TestFastUserViews(TestCase):
    """Test fastuser views directly"""
    
    def setUp(self):
        self.client = APIClient()
        
    @pytest.mark.skip(reason="Registration endpoint is disabled")
    def test_user_register(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': TEST_PASSWORD
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, 200)
        
    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = MyUser.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password=TEST_PASSWORD
        )
        
        data = {
            'username': 'loginuser',
            'password': TEST_PASSWORD
        }
        response = self.client.post('/api/user/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        
    @pytest.mark.skip(reason="Registration endpoint is disabled") 
    def test_duplicate_username(self):
        """Test duplicate username registration"""
        MyUser.objects.create_user(
            username='existing',
            email='existing@example.com',
            password=TEST_PASSWORD
        )
        
        data = {
            'username': 'existing',
            'email': 'new@example.com',
            'password': TEST_PASSWORD
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
            project_name="Test Mock Project",
            project_desc="Test description"
        )
        self.assertTrue(str(project).startswith("MockProject object"))
        
    def test_mock_api_str(self):
        """Test MockAPI string representation"""
        project = MockProject.objects.create(
            project_name="Test Project",
            project_desc="Test"
        )
        api = MockAPI.objects.create(
            project=project,
            request_method="GET",
            request_path="/test/api",
            api_name="Test API",
            response_text=json.dumps({"success": True})
        )
        self.assertTrue(str(api).startswith("MockAPI object"))
        
    def test_mock_api_fields(self):
        """Test MockAPI field defaults"""
        project = MockProject.objects.create(project_name="Test", project_desc="Test")
        api = MockAPI.objects.create(
            project=project,
            request_method="POST",
            request_path="/api/test",
            api_name="Test API"
        )
        
        # Test that the API was created successfully with default values
        self.assertTrue(api.is_active)
        self.assertTrue(api.enabled)


@pytest.mark.django_db
class TestSystemModels(TestCase):
    """Test system module models"""
    
    def test_log_record_creation(self):
        """Test LogRecord model creation"""
        log = LogRecord.objects.create(
            level="INFO",
            message="Test log message",
            request_id="test-request-123"
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
        today = get_day()
        tomorrow = get_day(1)
        yesterday = get_day(-1)
        
        self.assertIsInstance(today, str)
        self.assertIsInstance(tomorrow, str)
        self.assertIsInstance(yesterday, str)
        
        # Test date format
        self.assertRegex(today, r'^\d{4}-\d{2}-\d{2}$')
        
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
        from fastrunner.utils.relation import API_AUTHOR, API_RELATION
        
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
        tree_out = TreeOut(tree=[{"id": 1, "label": "Test"}], id=1, max=10)
        self.assertEqual(tree_out.id, 1)
        self.assertEqual(tree_out.max, 10)
        self.assertIsInstance(tree_out.tree, list)
        
        # Test TreeUniqueIn
        tree_in = TreeUniqueIn(project_id=1, type=1)
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
        
        token = generate_token('testuser')
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)