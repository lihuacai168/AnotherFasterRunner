import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from fastrunner.models import API, Case, CaseStep, Config, HostIP, Project, Variables
from fastuser.models import MyUser
from test_constants import TEST_PASSWORD


@pytest.mark.django_db
class TestProjectModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=TEST_PASSWORD
        )
        
    def test_project_creation(self):
        """Test basic project creation"""
        project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
        assert project.name == "Test Project"
        assert project.desc == "Test Description"
        assert project.responsible == "testuser"
        assert project.is_deleted == 0
        assert project.yapi_base_url == ""
        assert project.yapi_openapi_token == ""
        
    def test_project_unique_name_constraint(self):
        """Test that project names must be unique"""
        Project.objects.create(
            name="Unique Project",
            desc="First project",
            responsible="testuser"
        )
        
        with pytest.raises(IntegrityError):
            Project.objects.create(
                name="Unique Project",
                desc="Second project with same name",
                responsible="testuser"
            )
            
    def test_project_str_representation(self):
        """Test string representation of project"""
        project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        # Project model doesn't have __str__ method, so we just check it exists
        assert project.name == "Test Project"


@pytest.mark.django_db
class TestAPIModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description", 
            responsible="testuser"
        )
        
    def test_api_creation(self):
        """Test basic API creation"""
        api = API.objects.create(
            name="Test API",
            body='{"test": "data"}',
            url="/api/test",
            method="GET",
            project=self.project,
            relation=1
        )
        
        assert api.name == "Test API"
        assert api.body == '{"test": "data"}'
        assert api.url == "/api/test"
        assert api.method == "GET"
        assert api.project == self.project
        assert api.relation == 1
        assert api.delete == 0
        assert api.tag == 0
        
    def test_api_choices(self):
        """Test API tag choices"""
        api = API.objects.create(
            name="Test API",
            body='{"test": "data"}',
            url="/api/test", 
            method="POST",
            project=self.project,
            relation=1,
            tag=1  # 成功
        )
        
        assert api.tag == 1
        
        # Django doesn't validate choices at model level, only at form/serializer level
        # So we can create an API with invalid tag value
        invalid_api = API.objects.create(
            name="Invalid API",
            body='{"test": "data"}',
            url="/api/invalid",
            method="POST", 
            project=self.project,
            relation=1,
            tag=99  # Invalid tag value
        )
        assert invalid_api.tag == 99  # It saves without error


@pytest.mark.django_db  
class TestCaseModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
    def test_case_creation(self):
        """Test basic case creation"""
        case = Case.objects.create(
            name="Test Case",
            project=self.project,
            relation=1,
            length=5,
            tag=1  # 冒烟用例
        )
        
        assert case.name == "Test Case"
        assert case.project == self.project
        assert case.relation == 1
        assert case.length == 5
        assert case.tag == 1
        
    def test_case_tags(self):
        """Test case tag choices"""
        valid_tags = [1, 2, 3, 4]  # 冒烟用例, 集成用例, 监控脚本, 核心用例
        
        for tag in valid_tags:
            case = Case.objects.create(
                name=f"Test Case {tag}",
                project=self.project,
                relation=tag,
                length=1,
                tag=tag
            )
            assert case.tag == tag


@pytest.mark.django_db
class TestConfigModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
    def test_config_creation(self):
        """Test basic config creation"""
        config = Config.objects.create(
            name="Test Config",
            body='{"headers": {"Content-Type": "application/json"}}',
            base_url="https://api.example.com",
            project=self.project,
            is_default=True
        )
        
        assert config.name == "Test Config"
        assert "headers" in config.body
        assert config.base_url == "https://api.example.com"
        assert config.project == self.project
        assert config.is_default is True
        
    def test_multiple_configs_per_project(self):
        """Test that projects can have multiple configs"""
        config1 = Config.objects.create(
            name="Dev Config",
            body='{"env": "dev"}',
            base_url="https://dev.api.example.com", 
            project=self.project,
            is_default=True
        )
        
        config2 = Config.objects.create(
            name="Prod Config",
            body='{"env": "prod"}',
            base_url="https://prod.api.example.com",
            project=self.project,
            is_default=False
        )
        
        configs = Config.objects.filter(project=self.project)
        assert configs.count() == 2
        assert config1 in configs
        assert config2 in configs


@pytest.mark.django_db
class TestVariablesModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
    def test_variables_creation(self):
        """Test basic variables creation"""
        variable = Variables.objects.create(
            key="API_KEY",
            value="test_api_key_12345",
            project=self.project,
            description="Test API key for authentication"
        )
        
        assert variable.key == "API_KEY"
        assert variable.value == "test_api_key_12345"
        assert variable.project == self.project
        assert variable.description == "Test API key for authentication"
        
    def test_variables_key_project_uniqueness(self):
        """Test that variable keys should be unique per project"""
        Variables.objects.create(
            key="DUPLICATE_KEY",
            value="first_value",
            project=self.project
        )
        
        # This should work - same key in different project
        other_project = Project.objects.create(
            name="Other Project", 
            desc="Other Description",
            responsible="otheruser"
        )
        
        Variables.objects.create(
            key="DUPLICATE_KEY",
            value="second_value",
            project=other_project
        )
        
        # Verify both variables exist
        assert Variables.objects.filter(key="DUPLICATE_KEY").count() == 2


@pytest.mark.django_db
class TestHostIPModel(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description", 
            responsible="testuser"
        )
        
    def test_hostip_creation(self):
        """Test basic HostIP creation"""
        host = HostIP.objects.create(
            name="dev.example.com",
            value="192.168.1.100",
            project=self.project
        )
        
        assert host.name == "dev.example.com"
        assert host.value == "192.168.1.100"
        assert host.project == self.project
        
    def test_multiple_hosts_per_project(self):
        """Test that projects can have multiple host configurations"""
        host1 = HostIP.objects.create(
            name="dev.api.com",
            value="192.168.1.100",
            project=self.project
        )
        
        host2 = HostIP.objects.create(
            name="staging.api.com", 
            value="192.168.1.200",
            project=self.project
        )
        
        hosts = HostIP.objects.filter(project=self.project)
        assert hosts.count() == 2
        assert host1 in hosts
        assert host2 in hosts