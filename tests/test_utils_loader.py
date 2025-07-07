"""Comprehensive tests for fastrunner.utils.loader module to achieve 100% coverage"""
import copy
import datetime
import io
import json
import os
import shutil
import sys
import tempfile
import types
from concurrent.futures import Future
from unittest.mock import MagicMock, Mock, call, patch

import pytest
import yaml
from django.test import TestCase
from requests.cookies import RequestsCookieJar

from fastrunner import models
from fastrunner.utils import loader
from fastuser.models import MyUser


@pytest.mark.django_db
class TestLoaderUtils(TestCase):
    """Test all functions in loader module"""

    def setUp(self):
        """Set up test data"""
        self.user = MyUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass'
        )
        self.project = models.Project.objects.create(
            name="Test Project",
            desc="Test",
            responsible="testuser"
        )
        self.relation = models.Relation.objects.create(
            project=self.project,
            tree=json.dumps([{"id": 1, "label": "Test", "children": []}]),
            type=1
        )

    def test_is_function_true(self):
        """Test is_function returns True for functions"""
        def test_func():
            pass
        
        result = loader.is_function(("test_func", test_func))
        self.assertTrue(result)

    def test_is_function_false(self):
        """Test is_function returns False for non-functions"""
        test_var = "test"
        result = loader.is_function(("test_var", test_var))
        self.assertFalse(result)

    def test_is_variable_true(self):
        """Test is_variable returns True for variables"""
        test_var = "test"
        result = loader.is_variable(("test_var", test_var))
        self.assertTrue(result)

    def test_is_variable_false_callable(self):
        """Test is_variable returns False for callable"""
        def test_func():
            pass
        
        result = loader.is_variable(("test_func", test_func))
        self.assertFalse(result)

    def test_is_variable_false_module(self):
        """Test is_variable returns False for modules"""
        import os as test_module
        result = loader.is_variable(("test_module", test_module))
        self.assertFalse(result)

    def test_is_variable_false_private(self):
        """Test is_variable returns False for private variables"""
        _private_var = "test"
        result = loader.is_variable(("_private_var", _private_var))
        self.assertFalse(result)

    def test_is_variable_skip_tuple(self):
        """Test is_variable handling of tuples"""
        test_tuple = ("a", "b")
        # This will return True as tuples are not specifically excluded in is_variable
        result = loader.is_variable(("test_tuple", test_tuple))
        self.assertTrue(result)

    def test_file_loader_dump_yaml_file(self):
        """Test FileLoader.dump_yaml_file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            test_data = {"key": "value", "nested": {"inner": "data"}}
            loader.FileLoader.dump_yaml_file(f.name, test_data)
            
        with open(f.name, 'r') as f:
            loaded_data = yaml.safe_load(f)
            self.assertEqual(loaded_data, test_data)
        
        os.unlink(f.name)

    def test_file_loader_dump_json_file(self):
        """Test FileLoader.dump_json_file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {"key": "value", "nested": {"inner": "data"}}
            loader.FileLoader.dump_json_file(f.name, test_data)
            
        with open(f.name, 'r') as f:
            loaded_data = json.load(f)
            self.assertEqual(loaded_data, test_data)
        
        os.unlink(f.name)

    def test_file_loader_dump_python_file(self):
        """Test FileLoader.dump_python_file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            test_code = "def test_func():\n    return 'test'"
            loader.FileLoader.dump_python_file(f.name, test_code)
            
        with open(f.name, 'r') as f:
            loaded_code = f.read()
            self.assertEqual(loaded_code, test_code)
        
        os.unlink(f.name)

    def test_file_loader_dump_binary_file(self):
        """Test FileLoader.dump_binary_file"""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            test_data = b"binary test data"
            loader.FileLoader.dump_binary_file(f.name, test_data)
            
        with open(f.name, 'rb') as f:
            loaded_data = f.read()
            self.assertEqual(loaded_data, test_data)
        
        os.unlink(f.name)

    @patch('importlib.import_module')
    @patch('importlib.reload')
    def test_file_loader_load_python_module(self, mock_reload, mock_import):
        """Test FileLoader.load_python_module"""
        # Create mock module
        mock_module = Mock()
        mock_module.test_var = "test_value"
        mock_module.test_func = lambda: "test"
        mock_module._private = "private"
        mock_module.test_tuple = ("a", "b")
        
        # Set up module attributes
        mock_module.__dict__ = {
            'test_var': "test_value",
            'test_func': lambda: "test",
            '_private': "private",
            'test_tuple': ("a", "b"),
            'test_module': types.ModuleType('test')
        }
        
        mock_import.return_value = mock_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = loader.FileLoader.load_python_module(tmpdir)
            
            self.assertIn("variables", result)
            self.assertIn("functions", result)
            self.assertEqual(result["variables"]["test_var"], "test_value")
            self.assertIn("test_func", result["functions"])

    @patch('importlib.import_module')
    def test_file_loader_load_python_module_with_cache(self, mock_import):
        """Test FileLoader.load_python_module with cached module"""
        # Add module to sys.modules to test cache clearing
        sys.modules['debugtalk'] = Mock()
        
        mock_module = Mock()
        mock_module.__dict__ = {}
        mock_import.return_value = mock_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = loader.FileLoader.load_python_module(tmpdir)
            
            # Module should have been removed from cache
            self.assertIn("variables", result)
            self.assertIn("functions", result)

    def test_parse_validate_and_extract_with_string(self):
        """Test parse_validate_and_extract with string values"""
        list_of_dict = [{"key": "$var1"}, {"key2": "static"}]
        variables_mapping = {"var1": "value1"}
        functions_mapping = {}
        api_variables = [{"api_var": "api_value"}]
        
        with patch('httprunner.parser.parse_data') as mock_parse:
            mock_parse.side_effect = lambda d, **kwargs: d
            with patch('httprunner.parser.parse_string_functions') as mock_parse_func:
                mock_parse_func.side_effect = lambda v, **kwargs: v
                
                loader.parse_validate_and_extract(
                    list_of_dict, variables_mapping, functions_mapping, api_variables
                )
                
                # Should call parse_data for both items
                self.assertEqual(mock_parse.call_count, 2)

    def test_parse_validate_and_extract_with_list(self):
        """Test parse_validate_and_extract with list values (validate)"""
        list_of_dict = [{"equals": ["$var1", 123]}]
        variables_mapping = {"var1": "value1"}
        functions_mapping = {}
        api_variables = []
        
        with patch('httprunner.parser.parse_data') as mock_parse:
            mock_parse.return_value = {"equals": ["value1", 123]}
            with patch('httprunner.parser.parse_string_functions') as mock_parse_func:
                mock_parse_func.side_effect = lambda v, **kwargs: v
                
                loader.parse_validate_and_extract(
                    list_of_dict, variables_mapping, functions_mapping, api_variables
                )
                
                mock_parse.assert_called_once()

    def test_parse_validate_and_extract_skip_api_variables(self):
        """Test parse_validate_and_extract skips api variables"""
        list_of_dict = [{"key": "api_var"}]
        variables_mapping = {}
        functions_mapping = {}
        api_variables = [{"api_var": "value"}]
        
        with patch('httprunner.parser.parse_data') as mock_parse:
            loader.parse_validate_and_extract(
                list_of_dict, variables_mapping, functions_mapping, api_variables
            )
            
            # Should not call parse_data because api_var is in api_variables
            mock_parse.assert_not_called()

    def test_parse_validate_and_extract_exception_handling(self):
        """Test parse_validate_and_extract handles exceptions"""
        from httprunner.exceptions import FunctionNotFound, VariableNotFound
        
        list_of_dict = [{"key": "$missing_var"}]
        variables_mapping = {}
        functions_mapping = {}
        api_variables = []
        
        with patch('httprunner.parser.parse_data') as mock_parse:
            mock_parse.side_effect = VariableNotFound("missing_var")
            
            # Should not raise exception
            loader.parse_validate_and_extract(
                list_of_dict, variables_mapping, functions_mapping, api_variables
            )

    def test_parse_tests_basic(self):
        """Test parse_tests with basic testcases"""
        testcases = [{"name": "test1"}, {"name": "test2"}]
        debugtalk = {"functions": {"func1": lambda: "test"}, "variables": {"var1": "value1"}}
        
        result = loader.parse_tests(testcases, debugtalk)
        
        self.assertEqual(result["config"]["name"], "test2")
        self.assertEqual(result["teststeps"], testcases)
        self.assertIn("refs", result["config"])

    def test_parse_tests_with_config(self):
        """Test parse_tests with config"""
        testcases = [{"name": "test1"}]
        debugtalk = {}
        config = {"name": "config_name", "variables": [{"config_var": "config_value"}]}
        
        result = loader.parse_tests(testcases, debugtalk, config=config)
        
        self.assertEqual(result["config"]["name"], "config_name")
        self.assertIn({"config_var": "config_value"}, result["config"]["variables"])

    def test_parse_tests_with_name_override(self):
        """Test parse_tests with name override"""
        testcases = [{"name": "test1"}]
        debugtalk = {}
        config = {"name": "config_name"}
        
        result = loader.parse_tests(testcases, debugtalk, name="override_name", config=config)
        
        self.assertEqual(result["config"]["name"], "override_name")

    def test_parse_tests_with_global_variables(self):
        """Test parse_tests with global variables"""
        testcases = [{"name": "test1"}]
        debugtalk = {}
        
        # Create global variable
        models.Variables.objects.create(
            key="global_var",
            value="global_value",
            project=self.project
        )
        
        result = loader.parse_tests(testcases, debugtalk, project=self.project)
        
        # Check global variable is added
        self.assertIn({"global_var": "global_value"}, result["config"]["variables"])

    def test_parse_tests_with_extract_validate(self):
        """Test parse_tests with extract and validate"""
        testcases = [{
            "name": "test1",
            "extract": [{"token": "$response"}],
            "validate": [{"equals": ["$status", 200]}],
            "variables": [{"test_var": "test_value"}]
        }]
        debugtalk = {"functions": {}, "variables": {}}
        
        with patch('fastrunner.utils.loader.parse_validate_and_extract') as mock_parse:
            result = loader.parse_tests(testcases, debugtalk)
            
            # Should be called twice (once for extract, once for validate)
            self.assertEqual(mock_parse.call_count, 2)

    def test_load_debugtalk(self):
        """Test load_debugtalk function"""
        # Create debugtalk
        models.Debugtalk.objects.create(
            project=self.project,
            code="def test_func():\n    return 'test'\n\ntest_var = 'test_value'"
        )
        
        with patch('fastrunner.utils.loader.FileLoader.dump_python_file') as mock_dump:
            with patch('fastrunner.utils.loader.FileLoader.load_python_module') as mock_load:
                mock_load.return_value = {"functions": {"test_func": lambda: "test"}}
                
                result = loader.load_debugtalk(self.project.id)
                
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                mock_dump.assert_called_once()
                mock_load.assert_called_once()

    def test_load_debugtalk_exception(self):
        """Test load_debugtalk with exception"""
        models.Debugtalk.objects.create(
            project=self.project,
            code="invalid python code {"
        )
        
        with patch('fastrunner.utils.loader.FileLoader.dump_python_file'):
            with patch('fastrunner.utils.loader.FileLoader.load_python_module') as mock_load:
                mock_load.side_effect = Exception("Syntax error")
                
                result = loader.load_debugtalk(self.project.id)
                self.assertIsNone(result)

    def test_merge_parallel_result(self):
        """Test merge_parallel_result function"""
        results = [
            {
                "success": True,
                "stat": {"total": 10, "failures": 1, "errors": 0},
                "time": {"start_at": 1000, "duration": 5},
                "details": ["detail1"],
                "extra_key": "should_be_removed"
            },
            {
                "success": False,
                "stat": {"total": 5, "failures": 2, "errors": 1},
                "time": {"start_at": 900, "duration": 3},
                "details": ["detail2"],
                "platform": {"python": "3.9"}
            }
        ]
        duration = 10
        
        result = loader.merge_parallel_result(results, duration)
        
        self.assertFalse(result["success"])  # One failed, so overall false
        self.assertEqual(result["stat"]["total"], 15)
        self.assertEqual(result["stat"]["failures"], 3)
        self.assertEqual(result["time"]["start_at"], 900)  # Min start time
        self.assertEqual(result["time"]["duration"], 10)  # Provided duration
        self.assertEqual(len(result["details"]), 2)
        self.assertNotIn("extra_key", result)

    @patch('httprunner.api.HttpRunner')
    @patch('fastrunner.utils.loader.parse_summary')
    def test_debug_suite_parallel(self, mock_parse_summary, mock_runner_class):
        """Test debug_suite_parallel function"""
        test_sets = [
            {"config": {"name": "test1"}},
            {"config": {"name": "test2"}}
        ]
        
        # Mock runner
        mock_runner = Mock()
        mock_runner.summary = {"success": True}
        mock_runner_class.return_value = mock_runner
        
        # Mock parse_summary
        mock_parse_summary.return_value = {
            "success": True,
            "stat": {"total": 1, "failures": 0},
            "time": {"start_at": 1000, "duration": 1},
            "details": []
        }
        
        with patch('fastrunner.utils.loader.merge_parallel_result') as mock_merge:
            mock_merge.return_value = {"merged": True}
            
            result = loader.debug_suite_parallel(test_sets)
            
            self.assertEqual(result, {"merged": True})
            self.assertEqual(mock_runner_class.call_count, 2)

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('fastrunner.utils.loader.parse_tests')
    @patch('httprunner.api.HttpRunner')
    @patch('fastrunner.utils.loader.parse_summary')
    @patch('fastrunner.utils.loader.save_summary')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_suite_basic(self, mock_rmtree, mock_chdir, mock_save, mock_parse_summary, 
                               mock_runner_class, mock_parse_tests, mock_load_debugtalk):
        """Test debug_suite function"""
        suite = [[{"name": "test1"}]]
        obj = [{"case_id": 1, "name": "case1"}]
        config = [{"name": "config1"}]
        
        # Mock debugtalk
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        
        # Mock parse_tests
        mock_parse_tests.return_value = {"config": {"name": "test"}, "teststeps": []}
        
        # Mock runner
        mock_runner = Mock()
        mock_runner.summary = {"success": True}
        mock_runner_class.return_value = mock_runner
        
        # Mock parse_summary
        mock_parse_summary.return_value = {
            "success": True,
            "stat": {"total": 1, "failures": 0},
            "time": {},
            "details": [{
                "success": True,
                "records": [{
                    "meta_data": {
                        "response": {"json": {"test": "data"}}
                    }
                }]
            }]
        }
        
        # Mock save_summary
        mock_save.return_value = 123
        
        result, report_id = loader.debug_suite(
            suite, self.project.id, obj, config=config, save=True, user="test"
        )
        
        self.assertEqual(report_id, 123)
        self.assertIn("stat", result)
        self.assertIn("case_count", result["stat"])
        mock_save.assert_called_once()

    def test_debug_suite_empty_suite(self):
        """Test debug_suite with empty suite"""
        result = loader.debug_suite([], self.project.id, [])
        self.assertEqual(result, loader.TEST_NOT_EXISTS)

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('fastrunner.utils.loader.parse_tests')
    @patch('fastrunner.utils.loader.debug_suite_parallel')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_suite_parallel_mode(self, mock_rmtree, mock_chdir, mock_parallel, 
                                        mock_parse_tests, mock_load_debugtalk):
        """Test debug_suite with parallel mode"""
        suite = [[{"name": "test1"}]]
        obj = [{"case_id": 1, "name": "case1"}]
        config = [{"name": "config1"}]
        
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        mock_parse_tests.return_value = {"config": {"name": "test"}, "teststeps": []}
        mock_parallel.return_value = {
            "success": True,
            "stat": {},
            "details": []
        }
        
        result, _ = loader.debug_suite(
            suite, self.project.id, obj, config=config, save=False, allow_parallel=True
        )
        
        mock_parallel.assert_called_once()

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_suite_exception(self, mock_rmtree, mock_chdir, mock_load_debugtalk):
        """Test debug_suite with exception"""
        suite = [[{"name": "test1"}]]
        obj = [{"case_id": 1, "name": "case1"}]
        
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        
        with patch('fastrunner.utils.loader.parse_tests') as mock_parse:
            mock_parse.side_effect = Exception("Parse error")
            
            with self.assertRaises(SyntaxError):
                loader.debug_suite(suite, self.project.id, obj)
            
            # Cleanup should still be called
            mock_rmtree.assert_called_once()

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('fastrunner.utils.loader.parse_tests')
    @patch('httprunner.api.HttpRunner')
    @patch('fastrunner.utils.loader.parse_summary')
    @patch('fastrunner.utils.loader.save_summary')
    @patch('fastrunner.utils.loader.ConvertRequest.generate_curl')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_api_dict(self, mock_rmtree, mock_chdir, mock_curl, mock_save, 
                            mock_parse_summary, mock_runner_class, mock_parse_tests, mock_load_debugtalk):
        """Test debug_api with dict input"""
        api = {"name": "test_api", "request": {"url": "/test"}}
        
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        mock_parse_tests.return_value = {"config": {"name": "test"}, "teststeps": []}
        
        mock_runner = Mock()
        mock_runner.summary = {"success": True}
        mock_runner_class.return_value = mock_runner
        
        mock_parse_summary.return_value = {
            "success": True,
            "details": [{
                "records": [{
                    "meta_data": {
                        "response": {"json": {"test": "data"}}
                    }
                }]
            }]
        }
        
        result = loader.debug_api(api, self.project.id, name="test", save=True)
        
        self.assertIn("details", result)
        mock_save.assert_called_once()
        mock_curl.assert_called_once()

    def test_debug_api_empty(self):
        """Test debug_api with empty api"""
        result = loader.debug_api([], self.project.id)
        self.assertEqual(result, loader.TEST_NOT_EXISTS)

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('fastrunner.utils.loader.parse_tests')
    @patch('httprunner.api.HttpRunner')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_api_with_parameters(self, mock_rmtree, mock_chdir, mock_runner_class, 
                                        mock_parse_tests, mock_load_debugtalk):
        """Test debug_api with parameters"""
        api = [{
            "name": "test_api",
            "request": {
                "url": "/test",
                "params": {"param1": "$var1", "param2": ["$var2", "$var3"]}
            }
        }]
        config = {
            "parameters": [
                {"var1": "value1", "var2": "value2"},
                {"var3": "value3", "var4": "value4"}
            ]
        }
        
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        mock_parse_tests.return_value = {"config": {"name": "test"}, "teststeps": []}
        
        mock_runner = Mock()
        mock_runner.summary = {"success": True}
        mock_runner_class.return_value = mock_runner
        
        with patch('fastrunner.utils.loader.parse_summary') as mock_parse:
            mock_parse.return_value = {"success": True, "details": []}
            
            loader.debug_api(api, self.project.id, config=config, save=False)
            
            # Check that parameters were filtered
            call_args = mock_parse_tests.call_args[1]
            self.assertEqual(len(call_args["config"]["parameters"]), 2)

    @patch('fastrunner.utils.loader.load_debugtalk')
    @patch('os.chdir')
    @patch('shutil.rmtree')
    def test_debug_api_exception(self, mock_rmtree, mock_chdir, mock_load_debugtalk):
        """Test debug_api with exception"""
        api = [{"name": "test_api"}]
        
        mock_load_debugtalk.return_value = ({"functions": {}}, "/tmp/debugtalk.py")
        
        with patch('fastrunner.utils.loader.parse_tests') as mock_parse:
            mock_parse.side_effect = Exception("Parse error")
            
            with self.assertRaises(SyntaxError):
                loader.debug_api(api, self.project.id)
            
            # Cleanup should still be called
            mock_rmtree.assert_called_once()

    @patch('fastrunner.utils.parser.Format')
    def test_load_test_with_newbody(self, mock_format):
        """Test load_test with newBody"""
        test = {"newBody": {"test": "data"}}
        
        mock_format_instance = Mock()
        mock_format_instance.testcase = {"name": "test"}
        mock_format.return_value = mock_format_instance
        mock_format_instance.parse = Mock()
        
        result = loader.load_test(test)
        
        self.assertEqual(result, {"name": "test"})
        mock_format.assert_called_once_with({"test": "data"})

    def test_load_test_with_case_config(self):
        """Test load_test with case and config method"""
        # Create config
        config = models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body='{"name": "Test Config", "request": {}}'
        )
        
        test = {
            "case": 1,
            "body": {"name": "Test Config", "method": "config"}
        }
        
        result = loader.load_test(test, project=self.project)
        
        self.assertEqual(result["name"], "Test Config")

    def test_load_test_with_case_step(self):
        """Test load_test with case step"""
        # Create case and step
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        step = models.CaseStep.objects.create(
            case=case,
            name="Test Step",
            url="/test",
            method="GET",
            body='{"name": "Test Step"}',
            step=0
        )
        
        test = {
            "id": step.id,
            "case": case.id,
            "body": {"name": "New Name", "method": "GET"}
        }
        
        result = loader.load_test(test)
        
        self.assertEqual(result["name"], "New Name")

    def test_load_test_with_api(self):
        """Test load_test with API"""
        # Create API
        api = models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body='{"name": "Test API"}',
            relation=1
        )
        
        test = {
            "id": api.id,
            "body": {"name": "Test API", "method": "GET"}
        }
        
        result = loader.load_test(test)
        
        self.assertEqual(result["name"], "Test API")

    def test_load_test_with_config_no_case(self):
        """Test load_test with config but no case key"""
        # Create config
        config = models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body='{"name": "Test Config"}'
        )
        
        test = {
            "body": {"name": "Test Config", "method": "config"}
        }
        
        result = loader.load_test(test, project=self.project)
        
        self.assertEqual(result["name"], "Test Config")

    def test_back_async_decorator(self):
        """Test back_async decorator"""
        call_args = []
        
        @loader.back_async
        def test_func(arg1, arg2=None):
            call_args.append((arg1, arg2))
        
        # Call the decorated function
        test_func("test1", arg2="test2")
        
        # Give thread time to execute
        import time
        time.sleep(0.1)
        
        # Check function was called
        self.assertEqual(call_args, [("test1", "test2")])

    def test_parse_summary_basic(self):
        """Test parse_summary function"""
        summary = {
            "details": [{
                "records": [{
                    "meta_data": {
                        "request": {
                            "data": b"test data",
                            "cookies": RequestsCookieJar()
                        },
                        "response": {
                            "content": "test content",
                            "content_type": "application/json",
                            "body": b"response body"
                        }
                    }
                }]
            }]
        }
        
        result = loader.parse_summary(summary)
        
        # Check bytes are decoded
        self.assertEqual(
            result["details"][0]["records"][0]["meta_data"]["request"]["data"],
            "test data"
        )
        self.assertEqual(
            result["details"][0]["records"][0]["meta_data"]["response"]["body"],
            "response body"
        )

    def test_parse_summary_with_html(self):
        """Test parse_summary with HTML content"""
        summary = {
            "details": [{
                "records": [{
                    "meta_data": {
                        "request": {},
                        "response": {
                            "content": "<html><body>Test</body></html>",
                            "content_type": "text/html"
                        }
                    }
                }]
            }]
        }
        
        result = loader.parse_summary(summary)
        
        # Check HTML is prettified
        content = result["details"][0]["records"][0]["meta_data"]["response"]["content"]
        self.assertIn("<html>", content)
        self.assertIn("<body>", content)

    def test_parse_summary_with_cookies(self):
        """Test parse_summary with cookies"""
        cookies = RequestsCookieJar()
        cookies.set('test_cookie', 'test_value')
        
        summary = {
            "details": [{
                "records": [{
                    "meta_data": {
                        "request": {"cookies": cookies},
                        "response": {"cookies": cookies}
                    }
                }]
            }]
        }
        
        result = loader.parse_summary(summary)
        
        # Check cookies are converted to dict
        req_cookies = result["details"][0]["records"][0]["meta_data"]["request"]["cookies"]
        self.assertIsInstance(req_cookies, dict)
        self.assertEqual(req_cookies.get("test_cookie"), "test_value")

    def test_save_summary_basic(self):
        """Test save_summary function"""
        summary = {
            "success": True,
            "stat": {"total": 10, "failures": 0},
            "details": [{"test": "detail"}]
        }
        
        result = loader.save_summary("Test Report", summary, self.project.id, type=1, user="test")
        
        # Check report was created
        report = models.Report.objects.get(id=result)
        self.assertEqual(report.name, "Test Report")
        self.assertEqual(report.status, True)
        self.assertEqual(report.type, 1)
        
        # Check report detail was created
        detail = models.ReportDetail.objects.filter(report=report).first()
        self.assertIsNotNone(detail)

    def test_save_summary_with_status(self):
        """Test save_summary with status key (should skip)"""
        summary = {"status": "error"}
        
        result = loader.save_summary("Test", summary, self.project.id)
        
        self.assertIsNone(result)

    def test_save_summary_no_name(self):
        """Test save_summary with no name"""
        summary = {
            "success": True,
            "details": []
        }
        
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"
            
            result = loader.save_summary(None, summary, self.project.id)
            
            report = models.Report.objects.get(id=result)
            self.assertEqual(report.name, "2023-01-01 12:00:00")

    def test_save_summary_with_ci_metadata(self):
        """Test save_summary with CI metadata"""
        summary = {
            "success": True,
            "details": []
        }
        ci_metadata = {
            "ci_project_id": "123",
            "ci_job_id": "456"
        }
        
        result = loader.save_summary("Test", summary, self.project.id, ci_metadata=ci_metadata)
        
        report = models.Report.objects.get(id=result)
        self.assertEqual(report.ci_project_id, "123")
        self.assertEqual(report.ci_job_id, "456")

    @patch('fastrunner.utils.loader.debug_api')
    @patch('fastrunner.utils.loader.save_summary')
    def test_async_debug_api(self, mock_save, mock_debug):
        """Test async_debug_api function"""
        api = {"name": "test"}
        mock_debug.return_value = {"success": True}
        
        # The function is decorated with @back_async, so it runs in a thread
        loader.async_debug_api(api, self.project.id, "Test", config={"test": "config"})
        
        # Give thread time to execute
        import time
        time.sleep(0.1)
        
        mock_debug.assert_called_once_with(
            api, self.project.id, save=False, config={"test": "config"}
        )
        mock_save.assert_called_once()

    @patch('fastrunner.utils.loader.debug_suite')
    @patch('fastrunner.utils.loader.save_summary')
    def test_async_debug_suite(self, mock_save, mock_debug):
        """Test async_debug_suite function"""
        suite = [{"test": "data"}]
        obj = [{"case_id": 1}]
        mock_debug.return_value = ({"success": True}, 123)
        
        # The function is decorated with @back_async, so it runs in a thread
        loader.async_debug_suite(suite, self.project.id, "Report", obj, config={"test": "config"})
        
        # Give thread time to execute
        import time
        time.sleep(0.1)
        
        mock_debug.assert_called_once()
        mock_save.assert_called_once()