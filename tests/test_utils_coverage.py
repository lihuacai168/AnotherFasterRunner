"""Test for fastrunner utils modules to improve coverage"""
import json
import pytest
from django.test import TestCase
from unittest.mock import MagicMock, patch

from fastrunner.utils import response, host, tree, runner, prepare
from fastrunner.utils.parser import Format
from fastrunner.utils.loader import save_summary


@pytest.mark.django_db
class TestUtilsHost(TestCase):
    """Test host utility functions"""
    
    def test_parse_host_basic(self):
        """Test basic host parsing"""
        from fastrunner.utils.host import parse_host
        
        # Test with normal URL
        testcase = {"request": {"url": "/api/test"}}
        result = parse_host("https://example.com", testcase)
        self.assertEqual(result["request"]["url"], "https://example.com/api/test")
        
        # Test with empty host
        result = parse_host("", testcase)
        self.assertEqual(result["request"]["url"], "/api/test")
        
        # Test with "请选择"
        result = parse_host("请选择", testcase)
        self.assertEqual(result["request"]["url"], "/api/test")
        
        # Test with base_url in testcase
        testcase_with_base = {"request": {"base_url": "http://old.com"}}
        result = parse_host("http://new.com", testcase_with_base)
        self.assertEqual(result["request"]["base_url"], "http://new.com")


@pytest.mark.django_db
class TestUtilsTree(TestCase):
    """Test tree utility functions"""
    
    def test_get_tree_max_id(self):
        """Test getting max tree ID"""
        from fastrunner.utils.tree import get_tree_max_id
        
        # Empty tree
        self.assertEqual(get_tree_max_id([]), 0)
        
        # Single level tree
        tree = [{"id": 1}, {"id": 3}, {"id": 2}]
        self.assertEqual(get_tree_max_id(tree), 3)
        
        # Nested tree
        tree = [
            {"id": 1, "children": [{"id": 5}, {"id": 4}]},
            {"id": 2, "children": [{"id": 8, "children": [{"id": 10}]}]}
        ]
        self.assertEqual(get_tree_max_id(tree), 10)


@pytest.mark.django_db
class TestUtilsRunner(TestCase):
    """Test runner utility functions"""
    
    @patch('fastrunner.utils.runner.HttpRunner')
    def test_run_summary(self, mock_runner_class):
        """Test run_summary function"""
        from fastrunner.utils.runner import run_summary
        
        # Mock HttpRunner instance
        mock_instance = MagicMock()
        mock_instance.summary = {"success": True, "stat": {"total": 1}}
        mock_runner_class.return_value = mock_instance
        
        result = run_summary("test")
        self.assertIsNotNone(result)
        mock_runner_class.assert_called_once()
        
    def test_run_single(self):
        """Test run_single function"""
        from fastrunner.utils.runner import run_single
        
        with patch('fastrunner.utils.runner.HttpRunner') as mock_runner:
            mock_instance = MagicMock()
            mock_instance.summary = {"success": True}
            mock_runner.return_value = mock_instance
            
            result = run_single({})
            self.assertIsNotNone(result)


@pytest.mark.django_db
class TestUtilsPrepare(TestCase):
    """Test prepare utility functions"""
    
    def test_get_counter(self):
        """Test variable counter"""
        from fastrunner.utils.prepare import get_counter
        
        # Test with variables
        content = "Hello $name, your id is $id"
        variables = ["name", "id", "unused"]
        counter = get_counter(content, variables)
        self.assertEqual(counter, {"name": 1, "id": 1})
        
        # Test without variables
        content = "No variables here"
        counter = get_counter(content, [])
        self.assertEqual(counter, {})
        
    def test_is_json(self):
        """Test JSON validation"""
        from fastrunner.utils.prepare import is_json
        
        self.assertTrue(is_json('{"key": "value"}'))
        self.assertFalse(is_json('not json'))
        self.assertFalse(is_json(''))


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
        
        result = save_summary("Test Run", summary, project_id=1, type=1)
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