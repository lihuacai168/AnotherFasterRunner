"""Test for serializers and models to improve coverage"""
import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase

from fastrunner.models import API, Case, Config, Project, Relation, Report, Variables
from fastrunner.serializers import (
    APISerializer,
    CaseSerializer,
    CaseStepSerializer,
    ConfigSerializer,
    ProjectSerializer,
    RelationSerializer,
    ReportSerializer,
    VariablesSerializer,
)
from fastuser.models import MyUser


@pytest.mark.django_db
class TestSerializers(TestCase):
    """Test serializer methods"""
    
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='serializertest',
            email='serializer@test.com',
            password='test123'
        )
        self.project = Project.objects.create(
            name="Serializer Project",
            desc="Test",
            responsible="serializertest"
        )
        
    def test_project_serializer(self):
        """Test ProjectSerializer"""
        serializer = ProjectSerializer(instance=self.project)
        data = serializer.data
        self.assertEqual(data['name'], "Serializer Project")
        self.assertIn('id', data)
        
    def test_relation_serializer(self):
        """Test RelationSerializer with tree structure"""
        relation = Relation.objects.create(
            project=self.project,
            tree=1,
            name="Test Node",
            type=1
        )
        
        serializer = RelationSerializer(instance=relation)
        data = serializer.data
        self.assertEqual(data['label'], "Test Node")
        self.assertEqual(data['id'], f"{relation.tree}_{relation.type}")
        
    def test_api_serializer_with_body_parsing(self):
        """Test APISerializer body parsing"""
        api = API.objects.create(
            name="Test API",
            project=self.project,
            method="POST",
            url="/test",
            body=json.dumps({
                "name": "Test API",
                "request": {
                    "url": "/test",
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "json": {"test": "data"}
                },
                "validate": [{"equals": ["status_code", 200]}],
                "extract": [{"token": "content.token"}]
            }),
            relation=1
        )
        
        # Test serialization
        serializer = APISerializer(instance=api)
        data = serializer.data
        self.assertEqual(data['name'], "Test API")
        self.assertIsInstance(data['body'], dict)
        
    def test_case_serializer(self):
        """Test CaseSerializer"""
        case = Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        
        serializer = CaseSerializer(instance=case)
        data = serializer.data
        self.assertEqual(data['name'], "Test Case")
        self.assertIn('id', data)
        
    def test_config_serializer_body_format(self):
        """Test ConfigSerializer body formatting"""
        config = Config.objects.create(
            name="Test Config",
            project=self.project,
            body=json.dumps({
                "name": "Test Config",
                "request": {
                    "base_url": "http://test.com",
                    "headers": {"Authorization": "Bearer token"}
                },
                "variables": [{"env": "test"}]
            })
        )
        
        serializer = ConfigSerializer(instance=config)
        data = serializer.data
        self.assertEqual(data['name'], "Test Config")
        self.assertIsInstance(data['body'], dict)
        
    def test_variables_serializer(self):
        """Test VariablesSerializer"""
        var = Variables.objects.create(
            key="test_var",
            value="test_value",
            project=self.project,
            description="Test variable"
        )
        
        serializer = VariablesSerializer(instance=var)
        data = serializer.data
        self.assertEqual(data['key'], "test_var")
        self.assertEqual(data['value'], "test_value")
        
    def test_report_serializer(self):
        """Test ReportSerializer"""
        report = Report.objects.create(
            project=self.project,
            name="Test Report",
            type=1,
            status=True,
            creator=self.user.username,
            detail=json.dumps({
                "success": True,
                "stat": {"total": 10, "successes": 8, "failures": 2},
                "time": {"start_at": "2023-01-01", "duration": 60}
            })
        )
        
        serializer = ReportSerializer(instance=report)
        data = serializer.data
        self.assertEqual(data['name'], "Test Report")
        self.assertTrue(data['status'])


@pytest.mark.django_db
class TestModelMethods(TestCase):
    """Test model methods and properties"""
    
    def test_project_str(self):
        """Test Project string representation"""
        project = Project.objects.create(
            name="String Test Project",
            desc="Test",
            responsible="test"
        )
        self.assertEqual(str(project), "String Test Project")
        
    def test_api_str(self):
        """Test API string representation"""
        project = Project.objects.create(name="Test", desc="Test", responsible="test")
        api = API.objects.create(
            name="String Test API",
            project=project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        self.assertEqual(str(api), "String Test API")
        
    def test_case_str(self):
        """Test Case string representation"""
        project = Project.objects.create(name="Test", desc="Test", responsible="test")
        case = Case.objects.create(
            name="String Test Case",
            project=project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        self.assertEqual(str(case), "String Test Case")
        
    def test_config_str(self):
        """Test Config string representation"""
        project = Project.objects.create(name="Test", desc="Test", responsible="test")
        config = Config.objects.create(
            name="String Test Config",
            project=project,
            body="{}"
        )
        self.assertEqual(str(config), "String Test Config")
        
    def test_variables_str(self):
        """Test Variables string representation"""
        project = Project.objects.create(name="Test", desc="Test", responsible="test")
        var = Variables.objects.create(
            key="test_key",
            value="test_value",
            project=project
        )
        self.assertEqual(str(var), "test_key")
        
    def test_report_str(self):
        """Test Report string representation"""
        project = Project.objects.create(name="Test", desc="Test", responsible="test")
        report = Report.objects.create(
            project=project,
            name="String Test Report",
            type=1,
            status=True,
            creator="test",
            detail="{}"
        )
        self.assertEqual(str(report), "String Test Report")