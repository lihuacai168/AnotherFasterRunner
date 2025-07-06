"""
Pytest configuration and fixtures for AnotherFasterRunner tests
"""
import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner


def pytest_configure():
    """Configure Django settings for pytest"""
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='fake-key-for-tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='FasterRunner.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATE_CONTEXT_PROCESSORS=(
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'fastrunner',
            'fastuser',
            'mock',
            'system',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework.authentication.SessionAuthentication',
            ],
        }
    )
    
    django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Set up test database"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }


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