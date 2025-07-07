"""Test for remaining modules to achieve 100% coverage"""
import json
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from test_constants import TEST_PASSWORD

from fastrunner.models import API, Config, HostIP, Project, Variables
from fastrunner.utils.parser import Format
from fastrunner.utils.tree import get_tree_max_id
from fastrunner.views.config import (
    ConfigView,
    HostIPView,
    VariablesView,
    variables_add,
    variables_delete,
    variables_list,
    variables_update,
)
from fastuser.models import MyUser


def mock_request_log(func):
    """Mock request_log decorator"""
    return func


@pytest.mark.django_db
class TestConfigViewsComplete(TestCase):
    """Complete test coverage for config views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create_user(
            username='configuser',
            email='config@example.com',
            password=TEST_PASSWORD
        )
        self.project = Project.objects.create(
            name="Config Complete Project",
            desc="Test",
            responsible="configuser"
        )

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_config_add(self):
        """Test ConfigView add method"""
        from fastrunner.views.config import ConfigView
        
        request = self.factory.post('/api/config/')
        request.user = self.user
        request.data = {
            'name': 'New Config',
            'project': self.project.id,
            'body': json.dumps({
                "name": "New Config",
                "request": {"base_url": "http://newconfig.com"}
            })
        }
        
        view = ConfigView()
        response = view.add(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('config_id', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_config_update(self):
        """Test ConfigView update method"""
        from fastrunner.views.config import ConfigView
        
        config = Config.objects.create(
            name="Update Config",
            project=self.project,
            body=json.dumps({"name": "Update Config"})
        )
        
        request = self.factory.patch(f'/api/config/{config.id}/')
        request.user = self.user
        request.data = {
            'name': 'Updated Config',
            'body': json.dumps({"name": "Updated Config"})
        }
        
        view = ConfigView()
        response = view.update(request, pk=config.id)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_config_copy(self):
        """Test ConfigView copy method"""
        from fastrunner.views.config import ConfigView
        
        config = Config.objects.create(
            name="Copy Config",
            project=self.project,
            body=json.dumps({"name": "Copy Config"})
        )
        
        request = self.factory.post(f'/api/config/{config.id}/')
        request.user = self.user
        request.data = {'name': 'Copied Config'}
        
        view = ConfigView()
        response = view.copy(request, pk=config.id)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_config_delete(self):
        """Test ConfigView delete method"""
        from fastrunner.views.config import ConfigView
        
        config = Config.objects.create(
            name="Delete Config",
            project=self.project,
            body=json.dumps({"name": "Delete Config"})
        )
        
        request = self.factory.delete('/api/config/')
        request.user = self.user
        request.data = json.dumps([config.id])
        request.content_type = 'application/json'
        
        view = ConfigView()
        response = view.delete(request)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_host_ip_list(self):
        """Test HostIPView list method"""
        from fastrunner.views.config import HostIPView
        
        HostIP.objects.create(
            name="Test Host",
            host="http://testhost.com",
            description="Test"
        )
        
        request = self.factory.get('/api/host_ip/')
        request.user = self.user
        
        view = HostIPView()
        response = view.list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_host_ip_add(self):
        """Test HostIPView add method"""
        from fastrunner.views.config import HostIPView
        
        request = self.factory.post('/api/host_ip/')
        request.user = self.user
        request.data = {
            'name': 'New Host',
            'host': 'http://newhost.com',
            'description': 'New host for testing'
        }
        
        view = HostIPView()
        response = view.add(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_host_ip_update(self):
        """Test HostIPView update method"""
        from fastrunner.views.config import HostIPView
        
        host = HostIP.objects.create(
            name="Update Host",
            host="http://updatehost.com",
            description="Update"
        )
        
        request = self.factory.patch(f'/api/host_ip/{host.id}/')
        request.user = self.user
        request.data = {
            'host': 'http://updatedhost.com',
            'description': 'Updated description'
        }
        
        view = HostIPView()
        response = view.update(request, pk=host.id)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_host_ip_delete(self):
        """Test HostIPView delete method"""
        from fastrunner.views.config import HostIPView
        
        host = HostIP.objects.create(
            name="Delete Host",
            host="http://deletehost.com",
            description="Delete"
        )
        
        request = self.factory.delete('/api/host_ip/')
        request.user = self.user
        request.data = json.dumps([host.id])
        request.content_type = 'application/json'
        
        view = HostIPView()
        response = view.delete(request)
        
        self.assertEqual(response.status_code, 200)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_variables_list_function(self):
        """Test variables_list function"""
        Variables.objects.create(
            key="test_key",
            value="test_value",
            project=self.project
        )
        
        request = self.factory.get('/api/variables/')
        request.user = self.user
        request.query_params = {'project': self.project.id}
        
        response = variables_list(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('variables', response.data)

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_variables_add_function(self):
        """Test variables_add function"""
        request = self.factory.post('/api/variables/')
        request.user = self.user
        request.data = {
            'key': 'new_var',
            'value': 'new_value',
            'project': self.project.id
        }
        
        response = variables_add(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_variables_update_function(self):
        """Test variables_update function"""
        var = Variables.objects.create(
            key="update_var",
            value="old_value",
            project=self.project
        )
        
        request = self.factory.patch(f'/api/variables/{var.id}/')
        request.user = self.user
        request.data = {
            'value': 'new_value'
        }
        
        response = variables_update(request, pk=var.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_variables_delete_function(self):
        """Test variables_delete function"""
        var = Variables.objects.create(
            key="delete_var",
            value="delete_value",
            project=self.project
        )
        
        request = self.factory.delete('/api/variables/')
        request.user = self.user
        request.data = json.dumps([var.id])
        request.content_type = 'application/json'
        
        response = variables_delete(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    @patch('fastrunner.utils.decorator.request_log', mock_request_log)
    def test_variables_view_all(self):
        """Test VariablesView all method"""
        from fastrunner.views.config import VariablesView
        
        Variables.objects.create(
            key="view_var",
            value="view_value", 
            project=self.project
        )
        
        request = self.factory.get('/api/variables/')
        request.user = self.user
        request.query_params = {'project': self.project.id, 'type': ''}
        
        view = VariablesView()
        response = view.all(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)


@pytest.mark.django_db
class TestTemplatetagsAndUtils(TestCase):
    """Test templatetags and remaining utils"""
    
    def test_custom_tags(self):
        """Test custom template tags"""
        from fastrunner.templatetags.custom_tags import iteration, show_type
        
        # Test iteration tag
        result = iteration('123_1')
        self.assertEqual(result, '1')
        
        result = iteration('invalid')
        self.assertEqual(result, '')
        
        # Test show_type tag
        self.assertEqual(show_type(1), '调试')
        self.assertEqual(show_type(2), '异步')
        self.assertEqual(show_type(3), '定时')
        self.assertEqual(show_type(4), '部署')
        self.assertEqual(show_type(5), '其他')

    def test_get_tree_label(self):
        """Test get_tree_label function"""
        from fastrunner.utils.tree import get_tree_label
        
        tree_lis = [
            {
                "id": 1,
                "label": "Parent",
                "children": [
                    {"id": 2, "label": "Child1", "children": []},
                    {"id": 3, "label": "Child2", "children": []}
                ]
            }
        ]
        
        result = get_tree_label(tree_lis, "Child1")
        self.assertEqual(result, "Parent")
        
        result = get_tree_label(tree_lis, "Parent")
        self.assertEqual(result, "Parent")
        
        result = get_tree_label(tree_lis, "NotFound")
        self.assertEqual(result, "")

    def test_parser_edge_cases(self):
        """Test parser edge cases"""
        # Test with variables
        data = {
            "name": "Variable Test",
            "project": 1,
            "method": "POST",
            "url": "/api/$var",
            "request": {
                "json": {"key": "$value"},
                "params": {"params": {"p1": "$param1"}},
                "headers": {"header": {"X-Token": "$token"}}
            },
            "variables": [
                {"var": "test"},
                {"value": "data"},
                {"param1": "p1value"},
                {"token": "bearer123"}
            ]
        }
        
        formatter = Format(data)
        formatter.parse()
        
        self.assertIn("variables", formatter.testcase)
        
        # Test with setup/teardown hooks
        data['setup_hooks'] = ["${setup_func()}"]
        data['teardown_hooks'] = ["${teardown_func()}"]
        
        formatter = Format(data)
        formatter.parse()
        
        self.assertIn("setup_hooks", formatter.testcase)
        self.assertIn("teardown_hooks", formatter.testcase)


@pytest.mark.django_db
class TestFastUserViews(TestCase):
    """Test fastuser views"""
    
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_user_registration(self):
        """Test user registration view"""
        from fastuser.views import RegisterView
        
        request = self.factory.post('/api/user/register/')
        request.data = {
            'username': 'newuser',
            'password': TEST_PASSWORD,
            'email': 'newuser@example.com'
        }
        
        view = RegisterView()
        response = view.post(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    def test_user_login(self):
        """Test user login view"""
        from fastuser.views import LoginView
        
        # Create user first
        user = MyUser.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password=TEST_PASSWORD
        )
        
        request = self.factory.post('/api/user/login/')
        request.data = {
            'username': 'loginuser',
            'password': TEST_PASSWORD
        }
        
        view = LoginView()
        response = view.post(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_info(self):
        """Test get user info"""
        from fastuser.views import info
        
        user = MyUser.objects.create_user(
            username='infouser',
            email='info@example.com',
            password=TEST_PASSWORD
        )
        
        request = self.factory.get('/api/user/info/')
        request.user = user
        request.session = {}
        
        response = info(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'infouser')


@pytest.mark.django_db
class TestAdminModules(TestCase):
    """Test admin modules"""
    
    def test_fastrunner_admin(self):
        """Test fastrunner admin registrations"""
        from django.contrib import admin
        from fastrunner.models import (
            API,
            Case,
            CaseStep,
            Config,
            HostIP,
            Project,
            Relation,
            Report,
            ReportDetail,
            Variables,
            Visit,
        )
        
        # Check all models are registered
        self.assertIn(Project, admin.site._registry)
        self.assertIn(API, admin.site._registry)
        self.assertIn(Case, admin.site._registry)
        self.assertIn(CaseStep, admin.site._registry)
        self.assertIn(Config, admin.site._registry)
        self.assertIn(HostIP, admin.site._registry)
        self.assertIn(Relation, admin.site._registry)
        self.assertIn(Report, admin.site._registry)
        self.assertIn(ReportDetail, admin.site._registry)
        self.assertIn(Variables, admin.site._registry)
        self.assertIn(Visit, admin.site._registry)

    def test_fastuser_admin(self):
        """Test fastuser admin registrations"""
        from django.contrib import admin
        from fastuser.admin import MyUserAdmin
        from fastuser.models import MyUser, UserInfo, UserToken
        
        # Check models are registered
        self.assertIn(MyUser, admin.site._registry)
        self.assertIn(UserInfo, admin.site._registry)
        self.assertIn(UserToken, admin.site._registry)
        
        # Check MyUserAdmin configuration
        user_admin = admin.site._registry[MyUser]
        self.assertIsInstance(user_admin, MyUserAdmin)
        self.assertIn('is_superuser', user_admin.list_display)

    def test_mock_admin(self):
        """Test mock admin registrations"""
        from django.contrib import admin
        from mock.models import MockAPI, MockProject
        
        self.assertIn(MockProject, admin.site._registry)
        self.assertIn(MockAPI, admin.site._registry)


@pytest.mark.django_db
class TestAppConfigs(TestCase):
    """Test app configurations"""
    
    def test_fastrunner_app_config(self):
        """Test FastrunnerConfig"""
        from fastrunner.apps import FastrunnerConfig
        
        self.assertEqual(FastrunnerConfig.name, 'fastrunner')
        self.assertEqual(FastrunnerConfig.default_auto_field, 'django.db.models.BigAutoField')

    def test_fastuser_app_config(self):
        """Test FastuserConfig"""
        from fastuser.apps import FastuserConfig
        
        self.assertEqual(FastuserConfig.name, 'fastuser')
        self.assertEqual(FastuserConfig.default_auto_field, 'django.db.models.BigAutoField')

    def test_system_app_config(self):
        """Test SystemConfig"""
        from system.apps import SystemConfig
        
        self.assertEqual(SystemConfig.name, 'system')
        self.assertEqual(SystemConfig.default_auto_field, 'django.db.models.BigAutoField')

    def test_mock_app_config(self):
        """Test MockConfig"""
        from mock.apps import MockConfig
        
        self.assertEqual(MockConfig.name, 'mock')
        self.assertEqual(MockConfig.default_auto_field, 'django.db.models.BigAutoField')