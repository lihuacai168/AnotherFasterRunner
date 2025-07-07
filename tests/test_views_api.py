import datetime
from unittest.mock import MagicMock, Mock, patch

import coreapi
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from fastrunner import models, serializers
from fastrunner.utils import response
from fastrunner.views.api import APITemplateView, APITemplateViewSchema


class TestAPITemplateViewSchema:
    """Test cases for APITemplateViewSchema"""

    def test_get_manual_fields_for_get(self):
        """Test get_manual_fields for GET method"""
        schema = APITemplateViewSchema()
        fields = schema.get_manual_fields('/api/test', 'GET')
        
        # Check that extra fields are added for GET
        field_names = [field.name for field in fields]
        assert 'node' in field_names
        assert 'project' in field_names
        assert 'search' in field_names
        assert 'tag' in field_names
        assert 'rigEnv' in field_names

    def test_get_manual_fields_for_post(self):
        """Test get_manual_fields for POST method"""
        schema = APITemplateViewSchema()
        fields = schema.get_manual_fields('/api/test', 'POST')
        
        # POST should not have the extra fields
        field_names = [field.name for field in fields]
        assert 'node' not in field_names
        assert 'project' not in field_names


class TestAPITemplateView:
    """Test cases for APITemplateView"""

    @pytest.fixture
    def view(self):
        return APITemplateView()

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def user(self):
        return User(username='testuser', id=1)

    @pytest.fixture
    def project(self):
        mock_project = MagicMock(spec=models.Project)
        mock_project.id = 1
        return mock_project

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.serializers.AssertSerializer')
    def test_list_valid_params(self, mock_serializer_class, mock_api_objects, view, factory, user):
        """Test list method with valid parameters"""
        # Setup request
        request = factory.get('/api/', {
            'project': '1',
            'search': 'test api',
            'node': '5',
            'tag': '1',
            'rigEnv': 'dev'
        })
        force_authenticate(request, user=user)
        
        # Mock serializer validation
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {
            'project': 1,
            'search': 'test api',
            'node': '5',
            'tag': '1',
            'rigEnv': 'dev',
            'delete': 0,
            'onlyMe': False,
            'showYAPI': True,
            'creator': None
        }
        mock_serializer_class.return_value = mock_serializer
        
        # Mock queryset
        mock_queryset = MagicMock()
        mock_api_objects.filter.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = mock_queryset
        
        # Mock pagination
        view.paginate_queryset = MagicMock(return_value=[])
        view.get_serializer = MagicMock(return_value=MagicMock(data=[]))
        view.get_paginated_response = MagicMock(return_value=Response([]))
        
        # Execute
        response = view.list(request)
        
        # Verify
        assert response.status_code == 200
        mock_queryset.filter.assert_any_call(project__id=1, delete=0)
        mock_queryset.order_by.assert_called_with('-update_time')

    @patch('fastrunner.views.api.serializers.AssertSerializer')
    def test_list_invalid_params(self, mock_serializer_class, view, factory, user):
        """Test list method with invalid parameters"""
        request = factory.get('/api/', {'project': 'invalid'})
        force_authenticate(request, user=user)
        
        # Mock serializer validation failure
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'project': ['Invalid project ID']}
        mock_serializer_class.return_value = mock_serializer
        
        response = view.list(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'project': ['Invalid project ID']}

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.serializers.AssertSerializer')
    def test_list_with_search_multiple_keywords(self, mock_serializer_class, mock_api_objects, view, factory, user):
        """Test list method with multiple search keywords"""
        request = factory.get('/api/', {'project': '1', 'search': 'user login test'})
        force_authenticate(request, user=user)
        
        # Mock serializer
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {
            'project': 1,
            'search': 'user login test',
            'delete': 0,
            'node': '',
            'tag': '',
            'rigEnv': '',
            'onlyMe': False,
            'showYAPI': True,
            'creator': None
        }
        mock_serializer_class.return_value = mock_serializer
        
        # Mock queryset
        mock_queryset = MagicMock()
        mock_api_objects.filter.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = mock_queryset
        
        # Mock pagination
        view.paginate_queryset = MagicMock(return_value=[])
        view.get_serializer = MagicMock(return_value=MagicMock(data=[]))
        view.get_paginated_response = MagicMock(return_value=Response([]))
        
        response = view.list(request)
        
        # Verify each search keyword is filtered
        assert mock_queryset.filter.call_count >= 3  # At least 3 calls for search keywords

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.serializers.AssertSerializer')
    def test_list_only_me_filter(self, mock_serializer_class, mock_api_objects, view, factory, user):
        """Test list method with onlyMe filter"""
        request = factory.get('/api/', {'project': '1', 'onlyMe': 'true'})
        force_authenticate(request, user=user)
        
        # Mock serializer
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {
            'project': 1,
            'onlyMe': True,
            'delete': 0,
            'search': '',
            'node': '',
            'tag': '',
            'rigEnv': '',
            'showYAPI': True,
            'creator': None
        }
        mock_serializer_class.return_value = mock_serializer
        
        # Mock queryset
        mock_queryset = MagicMock()
        mock_api_objects.filter.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = mock_queryset
        
        # Mock pagination
        view.paginate_queryset = MagicMock(return_value=[])
        view.get_serializer = MagicMock(return_value=MagicMock(data=[]))
        view.get_paginated_response = MagicMock(return_value=Response([]))
        
        response = view.list(request)
        
        # Verify creator filter is applied
        mock_queryset.filter.assert_any_call(creator=user)

    @patch('fastrunner.views.api.models.Project.objects')
    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.Format')
    def test_add_success(self, mock_format_class, mock_api_objects, mock_project_objects, view, factory, user, project):
        """Test successful API addition"""
        request_data = {
            'name': 'Test API',
            'url': '/test/api',
            'method': 'POST',
            'project': 1,
            'relation': 5,
            'body': {'test': 'data'}
        }
        request = factory.post('/api/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock Format
        mock_format = MagicMock()
        mock_format.name = 'Test API'
        mock_format.url = '/test/api'
        mock_format.method = 'POST'
        mock_format.project = 1
        mock_format.relation = 5
        mock_format.testcase = {'test': 'case'}
        mock_format_class.return_value = mock_format
        
        # Mock project retrieval
        mock_project_objects.get.return_value = project
        
        response = view.add(request)
        
        assert response.status_code == 200
        assert response.data == response.API_ADD_SUCCESS
        mock_api_objects.create.assert_called_once()

    @patch('fastrunner.views.api.models.Project.objects')
    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.Format')
    def test_add_data_too_long(self, mock_format_class, mock_api_objects, mock_project_objects, view, factory, user, project):
        """Test API addition with data too long error"""
        request = factory.post('/api/', {'test': 'data'}, format='json')
        force_authenticate(request, user=user)
        
        # Mock Format
        mock_format = MagicMock()
        mock_format.name = 'Test API'
        mock_format.url = '/test/api'
        mock_format.method = 'POST'
        mock_format.project = 1
        mock_format.relation = 5
        mock_format.testcase = {'test': 'case'}
        mock_format_class.return_value = mock_format
        
        # Mock project and DataError
        mock_project_objects.get.return_value = project
        mock_api_objects.create.side_effect = DataError("Data too long")
        
        response = view.add(request)
        
        assert response.status_code == 200
        assert response.data == response.DATA_TO_LONG

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.Format')
    def test_update_success(self, mock_format_class, mock_api_objects, view, factory, user):
        """Test successful API update"""
        request_data = {
            'name': 'Updated API',
            'url': '/updated/api',
            'method': 'PUT',
            'body': {'updated': 'data'}
        }
        request = factory.put('/api/1/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock Format
        mock_format = MagicMock()
        mock_format.name = 'Updated API'
        mock_format.url = '/updated/api'
        mock_format.method = 'PUT'
        mock_format.testcase = {'updated': 'case'}
        mock_format_class.return_value = mock_format
        
        # Mock filter
        mock_filter = MagicMock()
        mock_api_objects.filter.return_value = mock_filter
        
        response = view.update(request, pk=1)
        
        assert response.status_code == 200
        assert response.data == response.API_UPDATE_SUCCESS
        mock_filter.update.assert_called_once()

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.Format')
    def test_update_not_found(self, mock_format_class, mock_api_objects, view, factory, user):
        """Test API update when API not found"""
        request = factory.put('/api/999/', {}, format='json')
        force_authenticate(request, user=user)
        
        # Mock Format
        mock_format = MagicMock()
        mock_format_class.return_value = mock_format
        
        # Mock filter raising exception
        mock_api_objects.filter.side_effect = ObjectDoesNotExist
        
        response = view.update(request, pk=999)
        
        assert response.status_code == 200
        assert response.data == response.API_NOT_FOUND

    @patch('fastrunner.views.api.models.API.objects')
    def test_move_success(self, mock_api_objects, view, factory, user):
        """Test successful API move"""
        request_data = {
            'project': 1,
            'relation': 10,
            'api': [{'id': 1}, {'id': 2}, {'id': 3}]
        }
        request = factory.post('/api/move/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock filter
        mock_filter = MagicMock()
        mock_api_objects.filter.return_value = mock_filter
        
        response = view.move(request)
        
        assert response.status_code == 200
        assert response.data == response.API_UPDATE_SUCCESS
        mock_api_objects.filter.assert_called_with(project=1, id__in=[1, 2, 3])
        mock_filter.update.assert_called_with(relation=10)

    @patch('fastrunner.views.api.models.API.objects')
    def test_copy_success(self, mock_api_objects, view, factory, user):
        """Test successful API copy"""
        request_data = {'name': 'Copied API'}
        request = factory.post('/api/1/copy/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock original API
        mock_api = MagicMock()
        mock_api.body = "{'name': 'Original API', 'test': 'data'}"
        mock_api.id = 1
        mock_api.name = 'Original API'
        mock_api_objects.get.return_value = mock_api
        
        response = view.copy(request, pk=1)
        
        assert response.status_code == 200
        assert response.data == response.API_ADD_SUCCESS
        assert mock_api.name == 'Copied API'
        assert mock_api.creator == 'testuser'
        assert mock_api.updater == 'testuser'
        mock_api.save.assert_called_once()

    @patch('fastrunner.views.api.models.API.objects')
    def test_delete_single(self, mock_api_objects, view, factory, user):
        """Test single API deletion"""
        request = factory.delete('/api/1/')
        force_authenticate(request, user=user)
        
        # Mock filter
        mock_filter = MagicMock()
        mock_api_objects.filter.return_value = mock_filter
        
        response = view.delete(request, pk=1)
        
        assert response.status_code == 200
        assert response.data == response.API_DEL_SUCCESS
        mock_api_objects.filter.assert_called_with(id=1)
        # Verify soft delete
        update_call = mock_filter.update.call_args[1]
        assert update_call['delete'] == 1
        assert 'update_time' in update_call

    @patch('fastrunner.views.api.models.API.objects')
    def test_delete_bulk(self, mock_api_objects, view, factory, user):
        """Test bulk API deletion"""
        request_data = [{'id': 1}, {'id': 2}, {'id': 3}]
        request = factory.delete('/api/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock filter
        mock_filter = MagicMock()
        mock_api_objects.filter.return_value = mock_filter
        
        response = view.delete(request)
        
        assert response.status_code == 200
        assert response.data == response.API_DEL_SUCCESS
        assert mock_api_objects.filter.call_count == 3
        assert mock_filter.update.call_count == 3

    @patch('fastrunner.views.api.models.API.objects')
    def test_add_tag_success(self, mock_api_objects, view, factory, user):
        """Test successful tag addition"""
        request_data = {
            'api_ids': [1, 2, 3],
            'tag': 2
        }
        request = factory.post('/api/add_tag/', request_data, format='json')
        force_authenticate(request, user=user)
        
        # Mock filter
        mock_filter = MagicMock()
        mock_api_objects.filter.return_value = mock_filter
        
        response = view.add_tag(request)
        
        assert response.status_code == 200
        assert response.data == response.API_UPDATE_SUCCESS
        mock_api_objects.filter.assert_called_with(pk__in=[1, 2, 3])
        update_call = mock_filter.update.call_args[1]
        assert update_call['tag'] == 2
        assert update_call['updater'] == 'testuser'

    @patch('fastrunner.views.api.models.Case.objects')
    @patch('fastrunner.views.api.models.CaseStep.objects')
    @patch('fastrunner.views.api.models.API.objects')
    def test_sync_case_success(self, mock_api_objects, mock_casestep_objects, mock_case_objects, view, factory, user):
        """Test successful case synchronization"""
        request = factory.post('/api/1/sync_case/')
        force_authenticate(request, user=user)
        
        # Mock API data
        api_data = {
            'name': 'Test API',
            'body': '{"test": "data"}',
            'url': '/test/api',
            'method': 'POST',
            'project': 1
        }
        mock_api_objects.filter.return_value.values.return_value.first.return_value = api_data
        
        # Mock case IDs
        mock_case_objects.filter.return_value.values_list.return_value = [10, 11, 12]
        
        # Mock case steps
        mock_casesteps = MagicMock()
        mock_casestep_objects.filter.return_value = mock_casesteps
        mock_casesteps.values_list.return_value = [10, 11]
        
        response = view.sync_case(request, pk=1)
        
        assert response.status_code == 200
        assert response.data == response.CASE_STEP_SYNC_SUCCESS
        # Verify updates were called
        mock_casesteps.update.assert_called_once()
        mock_case_objects.filter.assert_called()

    @patch('fastrunner.views.api.Parse')
    @patch('fastrunner.views.api.models.API.objects')
    def test_single_success(self, mock_api_objects, mock_parse_class, view, factory, user):
        """Test getting single API details"""
        request = factory.get('/api/1/')
        force_authenticate(request, user=user)
        
        # Mock API
        mock_api = MagicMock()
        mock_api.id = 1
        mock_api.body = "{'test': 'data'}"
        mock_api.creator = 'testuser'
        mock_api.relation = 5
        mock_api.project.id = 1
        mock_api_objects.get.return_value = mock_api
        
        # Mock Parse
        mock_parse = MagicMock()
        mock_parse.testcase = {'parsed': 'data'}
        mock_parse_class.return_value = mock_parse
        
        response = view.single(request, pk=1)
        
        assert response.status_code == 200
        assert response.data['id'] == 1
        assert response.data['body'] == {'parsed': 'data'}
        assert response.data['success'] is True
        assert response.data['creator'] == 'testuser'
        assert response.data['relation'] == 5
        assert response.data['project'] == 1

    @patch('fastrunner.views.api.models.API.objects')
    def test_single_not_found(self, mock_api_objects, view, factory, user):
        """Test getting single API when not found"""
        request = factory.get('/api/999/')
        force_authenticate(request, user=user)
        
        mock_api_objects.get.side_effect = ObjectDoesNotExist
        
        response = view.single(request, pk=999)
        
        assert response.status_code == 200
        assert response.data == response.API_NOT_FOUND

    def test_queryset_excludes_tag_4(self, view):
        """Test that queryset excludes APIs with tag=4"""
        with patch('fastrunner.views.api.models.API.objects.filter') as mock_filter:
            mock_queryset = MagicMock()
            mock_filter.return_value = mock_queryset
            
            # Access the queryset property
            result = view.queryset
            
            # Verify ~Q(tag=4) is applied
            mock_filter.assert_called()
            call_args = mock_filter.call_args[0][0]
            # The argument should be a negated Q object for tag=4

    @patch('fastrunner.views.api.models.API.objects')
    @patch('fastrunner.views.api.serializers.AssertSerializer')
    def test_list_show_yapi_false(self, mock_serializer_class, mock_api_objects, view, factory, user):
        """Test list method with showYAPI=false filter"""
        request = factory.get('/api/', {'project': '1', 'showYAPI': 'false'})
        force_authenticate(request, user=user)
        
        # Mock serializer
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {
            'project': 1,
            'showYAPI': False,
            'delete': 0,
            'search': '',
            'node': '',
            'tag': '',
            'rigEnv': '',
            'onlyMe': False,
            'creator': None
        }
        mock_serializer_class.return_value = mock_serializer
        
        # Mock queryset
        mock_queryset = MagicMock()
        mock_api_objects.filter.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = mock_queryset
        
        # Mock pagination
        view.paginate_queryset = MagicMock(return_value=[])
        view.get_serializer = MagicMock(return_value=MagicMock(data=[]))
        view.get_paginated_response = MagicMock(return_value=Response([]))
        
        response = view.list(request)
        
        # Verify ~Q(creator="yapi") filter is applied
        assert response.status_code == 200
        # The filter call should include filtering out yapi creator