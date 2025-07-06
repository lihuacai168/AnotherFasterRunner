import json
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from fastrunner.models import API, Config, Project
from fastuser.models import MyUser


@pytest.mark.django_db
class TestProjectAPIViews(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com', 
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
    def test_project_list_view(self):
        """Test project list endpoint"""
        url = reverse('project-list')  # Adjust URL name based on your urls.py
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check if our test project is in the response
        response_data = response.json()
        assert 'results' in response_data or isinstance(response_data, list)
        
    def test_project_create_view(self):
        """Test project creation endpoint"""
        url = reverse('project-add')  # Adjust URL name based on your urls.py
        data = {
            'name': 'New Test Project',
            'desc': 'New project description',
            'responsible': 'testuser'
        }
        
        response = self.client.post(url, data, format='json')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        assert Project.objects.filter(name='New Test Project').exists()
        
    @pytest.mark.django_db
    def test_project_create_duplicate_name(self):
        """Test creating project with duplicate name"""
        url = reverse('project-add')
        data = {
            'name': 'Test Project',  # Same as existing project
            'desc': 'Duplicate project',
            'responsible': 'testuser'
        }
        
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        
        # Should return error for duplicate name
        assert response_data.get('success') is False
        assert 'exists' in response_data.get('msg', '').lower() or response_data.get('code') == '0101'


@pytest.mark.django_db
class TestAPITemplateViews(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description", 
            responsible="testuser"
        )
        
        self.api = API.objects.create(
            name="Test API",
            body='{"method": "GET", "url": "/test"}',
            url="/api/test",
            method="GET",
            project=self.project,
            relation=1,
            creator=self.user
        )
        
    def test_api_list_view(self):
        """Test API list endpoint with project filter"""
        url = reverse('api-list')  # Adjust URL name based on your urls.py
        response = self.client.get(url, {'project': self.project.id})
        
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Check if our test API is in the response
        if 'results' in response_data:
            apis = response_data['results']
        else:
            apis = response_data
            
        assert len(apis) >= 1
        api_names = [api['name'] for api in apis]
        assert 'Test API' in api_names
        
    def test_api_list_search_filter(self):
        """Test API list with search filter"""
        url = reverse('api-list')
        response = self.client.get(url, {
            'project': self.project.id,
            'search': 'Test'
        })
        
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        # Should return our test API
        if 'results' in response_data:
            apis = response_data['results'] 
        else:
            apis = response_data
            
        assert len(apis) >= 1
        
    def test_api_list_search_no_results(self):
        """Test API list with search that returns no results"""
        url = reverse('api-list')
        response = self.client.get(url, {
            'project': self.project.id,
            'search': 'NonExistentAPI'
        })
        
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        if 'results' in response_data:
            apis = response_data['results']
        else:
            apis = response_data
            
        assert len(apis) == 0
        
    def test_api_create_view(self):
        """Test API creation endpoint"""
        url = reverse('api-add')  # Adjust URL name based on your urls.py
        data = {
            'name': 'New Test API',
            'body': '{"method": "POST", "url": "/new-test"}',
            'url': '/api/new-test',
            'method': 'POST',
            'project': self.project.id,
            'relation': 1
        }
        
        response = self.client.post(url, data, format='json')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        assert API.objects.filter(name='New Test API').exists()
        
    def test_api_update_view(self):
        """Test API update endpoint"""
        url = reverse('api-update', kwargs={'pk': self.api.id})  # Adjust URL name
        data = {
            'name': 'Updated Test API',
            'body': '{"method": "PUT", "url": "/updated-test"}',
            'url': '/api/updated-test',
            'method': 'PUT',
            'project': self.project.id,
            'relation': 1
        }
        
        response = self.client.put(url, data, format='json')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        
        # Check that the API was updated
        updated_api = API.objects.get(id=self.api.id)
        assert updated_api.name == 'Updated Test API'
        assert updated_api.method == 'PUT'
        
    def test_api_delete_view(self):
        """Test API deletion endpoint"""
        url = reverse('api-delete', kwargs={'pk': self.api.id})  # Adjust URL name
        
        response = self.client.delete(url)
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        
        # Check that the API was soft deleted (delete=1) or hard deleted
        try:
            deleted_api = API.objects.get(id=self.api.id)
            assert deleted_api.delete == 1  # Soft delete
        except API.DoesNotExist:
            # Hard delete - that's also fine
            pass


@pytest.mark.django_db  
class TestConfigViews(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser" 
        )
        
        self.config = Config.objects.create(
            name="Test Config",
            body='{"headers": {"Content-Type": "application/json"}}',
            base_url="https://api.example.com",
            project=self.project,
            is_default=True
        )
        
    def test_config_list_view(self):
        """Test config list endpoint"""
        url = reverse('config-list')  # Adjust URL name based on your urls.py
        response = self.client.get(url, {'project': self.project.id})
        
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        
        if 'results' in response_data:
            configs = response_data['results']
        else:
            configs = response_data
            
        assert len(configs) >= 1
        config_names = [config['name'] for config in configs]
        assert 'Test Config' in config_names
        
    def test_config_create_view(self):
        """Test config creation endpoint"""
        url = reverse('config-add')  # Adjust URL name
        data = {
            'name': 'New Test Config',
            'body': '{"timeout": 30}',
            'base_url': 'https://new.api.example.com',
            'project': self.project.id,
            'is_default': False
        }
        
        response = self.client.post(url, data, format='json')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        assert Config.objects.filter(name='New Test Config').exists()
        
    def test_config_create_duplicate_name(self):
        """Test creating config with duplicate name in same project"""
        url = reverse('config-add')
        data = {
            'name': 'Test Config',  # Same as existing config
            'body': '{"duplicate": true}',
            'base_url': 'https://duplicate.api.example.com',
            'project': self.project.id,
            'is_default': False
        }
        
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        
        # Should return error for duplicate name
        assert response_data.get('success') is False
        assert 'exists' in response_data.get('msg', '').lower() or response_data.get('code') == '0101'


@pytest.mark.django_db
class TestAuthenticationRequired(APITestCase):
    
    def setUp(self):
        """Set up test data without authentication"""
        self.client = APIClient()
        self.project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        
    def test_unauthenticated_project_list(self):
        """Test that unauthenticated requests are rejected"""
        url = reverse('project-list')
        response = self.client.get(url)
        
        # Should require authentication
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        
    def test_unauthenticated_api_list(self):
        """Test that unauthenticated API requests are rejected"""
        url = reverse('api-list')
        response = self.client.get(url, {'project': self.project.id})
        
        # Should require authentication
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestErrorHandling(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_project_not_found(self):
        """Test handling of non-existent project"""
        url = reverse('api-list')
        response = self.client.get(url, {'project': 99999})  # Non-existent project
        
        # Should handle gracefully, not crash
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
    def test_invalid_data_format(self):
        """Test handling of invalid JSON data"""
        url = reverse('project-add')
        
        # Send invalid data
        response = self.client.post(url, {}, format='json')
        
        # Should return validation error, not crash
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK]
        
        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()
            assert response_data.get('success') is False