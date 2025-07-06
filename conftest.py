"""
Pytest configuration and fixtures for AnotherFasterRunner tests
"""
import os

import django
import pytest
from django.conf import settings
from django.test.utils import get_runner


def pytest_configure(config):
    """Configure pytest settings"""
    # Set up Django configuration first
    import os
    
    # Use CI settings if available, otherwise fall back to dev settings
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        pass  # Use existing setting
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FasterRunner.settings.dev')
    
    # Configure Django
    import django
    from django.conf import settings
    
    if not settings.configured:
        django.setup()




@pytest.fixture
def api_client():
    """Create API client for testing"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_user():
    """Create authenticated user for testing"""
    from fastuser.models import MyUser
    user = MyUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    """Create authenticated API client"""
    api_client.force_authenticate(user=authenticated_user)
    return api_client


@pytest.fixture
def sample_project(authenticated_user):
    """Create sample project for testing"""
    from fastrunner.models import Project
    return Project.objects.create(
        name="Test Project",
        desc="Test Description",
        responsible=authenticated_user.username
    )


@pytest.fixture
def sample_api(sample_project, authenticated_user):
    """Create sample API for testing"""
    from fastrunner.models import API
    return API.objects.create(
        name="Test API",
        body='{"method": "GET", "url": "/test"}',
        url="/api/test",
        method="GET",
        project=sample_project,
        relation=1,
        creator=authenticated_user
    )


@pytest.fixture
def sample_config(sample_project):
    """Create sample config for testing"""
    from fastrunner.models import Config
    return Config.objects.create(
        name="Test Config",
        body='{"headers": {"Content-Type": "application/json"}}',
        base_url="https://api.example.com",
        project=sample_project,
        is_default=True
    )


# Test markers for categorizing tests
pytest.mark.unit = pytest.mark.mark('unit')
pytest.mark.integration = pytest.mark.mark('integration')
pytest.mark.slow = pytest.mark.mark('slow')