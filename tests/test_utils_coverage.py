"""Test for fastrunner utils modules to improve coverage"""
import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase

from fastrunner.utils import host, prepare, response, runner, tree
from fastrunner.utils.loader import save_summary
from fastrunner.utils.parser import Format


@pytest.mark.django_db
class TestUtilsHost(TestCase):
    """Test host utility functions"""
    
    def test_parse_host_basic(self):
        """Test basic host parsing"""
        from fastrunner.utils.host import parse_host
        
        # Test with list of IPs
        testcase = {"request": {"url": "http://example.com/api/test"}}
        result = parse_host(["192.168.1.1"], testcase)
        self.assertIn("request", result)
        
        # Test with non-list IP (should return original)
        result = parse_host("not a list", testcase)
        self.assertEqual(result, testcase)
        
        # Test with empty API
        result = parse_host(["192.168.1.1"], None)
        self.assertIsNone(result)


@pytest.mark.django_db
class TestUtilsTree(TestCase):
    """Test tree utility functions"""
    
    def test_get_tree_max_id(self):
        """Test getting max tree ID"""
        from fastrunner.utils.tree import get_tree_max_id
        
        # Empty tree
        self.assertEqual(get_tree_max_id([]), 0)
        
        # Single level tree - need children field
        tree = [{"id": 1, "children": []}, {"id": 3, "children": []}, {"id": 2, "children": []}]
        self.assertEqual(get_tree_max_id(tree), 3)
        
        # Nested tree - all nodes need children field
        tree = [
            {"id": 1, "children": [{"id": 5, "children": []}, {"id": 4, "children": []}]},
            {"id": 2, "children": [{"id": 8, "children": [{"id": 10, "children": []}]}]}
        ]
        self.assertEqual(get_tree_max_id(tree), 10)


@pytest.mark.django_db
class TestUtilsRunner(TestCase):
    """Test runner utility functions"""
    
    def test_debug_code(self):
        """Test DebugCode class"""
        from fastrunner.utils.runner import DebugCode
        
        # Test initialization
        code = "print('hello')"
        debug = DebugCode(code)
        self.assertIsNotNone(debug)
        self.assertTrue(debug.temp.startswith('/tmp/FasterRunner'))


@pytest.mark.django_db
class TestUtilsPrepare(TestCase):
    """Test prepare utility functions"""
    
    def test_get_counter(self):
        """Test model counter"""
        from fastrunner.utils.prepare import get_counter
        from fastrunner.models import API
        
        # Test counter without project
        count = get_counter(API)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)
        
    def test_report_status_count(self):
        """Test report status counting"""
        from fastrunner.utils.prepare import report_status_count
        from fastrunner.models import Project
        
        # Create test project
        project = Project.objects.create(
            name="Test", 
            desc="Test", 
            responsible="test"
        )
        
        fail_count, success_count = report_status_count(project.id)
        self.assertEqual(fail_count, 0)
        self.assertEqual(success_count, 0)


@pytest.mark.django_db
class TestUtilsParser(TestCase):
    """Test parser utility functions"""
    
    def test_format_basic(self):
        """Test basic Format parsing"""
        data = {
            "name": "Test API",
            "project": 1,
            "relation": 1,
            "method": "GET",
            "url": "/test"
        }
        
        formatter = Format(data)
        self.assertEqual(formatter.name, "Test API")
        self.assertEqual(formatter.method, "GET")
        self.assertEqual(formatter.url, "/test")
        
    def test_format_parse(self):
        """Test Format parse method"""
        data = {
            "name": "Test",
            "project": 1,
            "method": "POST",
            "url": "/api/test",
            "header": {
                "header": {"Content-Type": "application/json"},
                "desc": {}
            },
            "request": {
                "json": {"test": "data"},
                "params": {"params": {}, "desc": {}}
            }
        }
        
        formatter = Format(data)
        formatter.parse()
        self.assertIsInstance(formatter.testcase, dict)
        self.assertIn("name", formatter.testcase)


@pytest.mark.django_db
class TestUtilsLoader(TestCase):
    """Test loader utility functions"""
    
    @patch('fastrunner.models.Report')
    def test_save_summary(self, mock_report):
        """Test save_summary function"""
        summary = {
            "success": True,
            "stat": {"total": 5, "successes": 4, "failures": 1},
            "time": {"start_at": "2023-01-01", "duration": 60},
            "details": []
        }
        
        result = save_summary("Test Run", summary, project=1, type=1)
        self.assertIsNotNone(result)
        mock_report.objects.create.assert_called_once()


@pytest.mark.django_db
class TestResponseConstants(TestCase):
    """Test all response constants are properly defined"""
    
    def test_success_responses(self):
        """Test success response constants"""
        success_responses = [
            response.SYSTEM_SUCCESS,
            response.PROJECT_ADD_SUCCESS,
            response.PROJECT_UPDATE_SUCCESS,
            response.PROJECT_DELETE_SUCCESS,
            response.TREE_ADD_SUCCESS,
            response.TREE_UPDATE_SUCCESS,
            response.TREE_DELETE_SUCCESS,
            response.API_ADD_SUCCESS,
            response.API_UPDATE_SUCCESS,
            response.API_DELETE_SUCCESS,
            response.CASE_ADD_SUCCESS,
            response.CASE_UPDATE_SUCCESS,
            response.CASE_DELETE_SUCCESS,
            response.CONFIG_ADD_SUCCESS,
            response.CONFIG_UPDATE_SUCCESS,
            response.CONFIG_DELETE_SUCCESS,
            response.REPORT_DELETE_SUCCESS,
            response.SCHEDULE_ADD_SUCCESS,
            response.SCHEDULE_UPDATE_SUCCESS,
            response.SCHEDULE_DELETE_SUCCESS,
            response.DEBUG_TALK_SUCCESS,
            response.HOST_ADD_SUCCESS,
            response.HOST_UPDATE_SUCCESS,
            response.HOST_DELETE_SUCCESS,
            response.VARIABLES_ADD_SUCCESS,
            response.VARIABLES_UPDATE_SUCCESS,
            response.VARIABLES_DELETE_SUCCESS,
        ]
        
        for resp in success_responses:
            self.assertTrue(resp['success'])
            self.assertEqual(resp['code'], '0001')
            
    def test_error_responses(self):
        """Test error response constants"""
        error_responses = [
            response.SYSTEM_ERROR,
            response.VALIDATE_ERROR,
            response.AUTH_FAIL,
            response.PROJECT_EXISTS,
            response.PROJECT_NOT_EXISTS,
            response.TREE_NOT_EXISTS,
            response.API_NOT_FOUND,
            response.DATA_TO_LONG,
            response.FILE_UPLOAD_ERROR,
            response.FILE_EXISTS,
            response.CASE_NOT_EXISTS,
            response.CASE_STEP_NOT_EXIST,
            response.CONFIG_NOT_EXISTS,
            response.CONFIG_IS_USED,
            response.REPORT_NOT_EXISTS,
            response.TASK_NOT_EXIST,
            response.TASK_HAS_EXISTS,
            response.TASK_HAS_RUN,
            response.SCHEDULE_NOT_EXISTS,
            response.HOST_NOT_EXISTS,
            response.VARIABLES_NOT_EXISTS,
        ]
        
        for resp in error_responses:
            self.assertFalse(resp['success'])
            self.assertIn('msg', resp)