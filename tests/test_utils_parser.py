"""Comprehensive tests for fastrunner.utils.parser module to achieve 100% coverage"""
import datetime
import json
from enum import Enum
from unittest.mock import MagicMock, Mock, call, patch

import pytest
import requests
from django.test import TestCase
from requests.cookies import RequestsCookieJar

from fastrunner import models
from fastrunner.utils import parser
from fastrunner.utils.parser import (
    FileType,
    Format,
    Parse,
    Yapi,
    format_json,
    format_summary_to_ding,
    set_customized_variable,
    yapi_properties2json,
)
from fastuser.models import MyUser


@pytest.mark.django_db
class TestFileType(TestCase):
    """Test FileType enum"""

    def test_file_type_values(self):
        """Test FileType enum values"""
        self.assertEqual(FileType.string.value, 1)
        self.assertEqual(FileType.int.value, 2)
        self.assertEqual(FileType.float.value, 3)
        self.assertEqual(FileType.bool.value, 4)
        self.assertEqual(FileType.list.value, 5)
        self.assertEqual(FileType.dict.value, 6)
        self.assertEqual(FileType.file.value, 7)


@pytest.mark.django_db
class TestFormat(TestCase):
    """Test Format class"""

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

    def test_format_init_test_level(self):
        """Test Format initialization with test level"""
        body = {
            "name": "Test API",
            "url": "/test",
            "method": "POST",
            "times": 3,
            "project": 1,
            "nodeId": 123,
            "rig_id": "rig123",
            "rig_env": 1,
            "header": {"header": {"Content-Type": "application/json"}, "desc": {"Content-Type": "Header desc"}},
            "request": {
                "params": {"params": {"key": "value"}, "desc": {"key": "Param desc"}},
                "form": {"data": {"form_key": "form_value"}, "desc": {"form_key": "Form desc"}},
                "json": {"json_key": "json_value"},
                "files": {"files": {"file_key": "file_path"}, "desc": {"file_key": "File desc"}}
            },
            "extract": {"extract": [{"token": "$.response.token"}], "desc": {"token": "Token desc"}},
            "validate": {"validate": [{"equals": ["status_code", 200]}]},
            "variables": {"variables": [{"var1": "value1"}], "desc": {"var1": "Variable desc"}},
            "hooks": {"setup_hooks": ["setup_func"], "teardown_hooks": ["teardown_func"]}
        }
        
        format_obj = Format(body, level="test")
        
        self.assertEqual(format_obj.name, "Test API")
        self.assertEqual(format_obj.url, "/test")
        self.assertEqual(format_obj.method, "POST")
        self.assertEqual(format_obj.project, 1)
        self.assertEqual(format_obj.relation, 123)
        self.assertEqual(format_obj.rig_id, "rig123")
        self.assertEqual(format_obj.rig_env, 1)

    def test_format_init_config_level(self):
        """Test Format initialization with config level"""
        body = {
            "name": "Test Config",
            "base_url": "http://test.com",
            "is_default": True,
            "header": {"header": {"Authorization": "Bearer token"}, "desc": {"Authorization": "Auth desc"}},
            "variables": {"variables": [{"env": "test"}], "desc": {"env": "Environment"}},
            "parameters": {"parameters": [{"param1": "value1"}], "desc": {"param1": "Param desc"}},
            "hooks": {"setup_hooks": ["setup"], "teardown_hooks": ["teardown"]}
        }
        
        format_obj = Format(body, level="config")
        
        self.assertEqual(format_obj.name, "Test Config")
        self.assertEqual(format_obj.base_url, "http://test.com")
        self.assertEqual(format_obj.is_default, True)

    def test_format_parse_test_level(self):
        """Test Format.parse() with test level"""
        body = {
            "name": "Test API",
            "url": "/test",
            "method": "GET",
            "times": 2,
            "rig_id": "test_rig",
            "header": {"header": {"Accept": "application/json"}},
            "request": {
                "params": {"params": {"q": "search"}},
                "form": {"data": {"username": "test"}},
                "json": {"key": "value"},
                "files": {"files": {"upload": "file.txt"}}
            },
            "extract": {"extract": [{"var": "$.data"}]},
            "validate": {"validate": [{"equals": ["status", "success"]}]},
            "variables": {"variables": [{"timeout": 30}]},
            "hooks": {"setup_hooks": ["setup"], "teardown_hooks": ["teardown"]}
        }
        
        format_obj = Format(body, level="test")
        format_obj.parse()
        
        result = format_obj.testcase
        self.assertEqual(result["name"], "Test API")
        self.assertEqual(result["times"], 2)
        self.assertEqual(result["rig_id"], "test_rig")
        self.assertEqual(result["request"]["url"], "/test")
        self.assertEqual(result["request"]["method"], "GET")
        self.assertFalse(result["request"]["verify"])
        self.assertIn("headers", result["request"])
        self.assertIn("params", result["request"])
        self.assertIn("data", result["request"])
        self.assertIn("json", result["request"])
        self.assertIn("files", result["request"])
        self.assertIn("extract", result)
        self.assertIn("validate", result)
        self.assertIn("variables", result)
        self.assertIn("setup_hooks", result)
        self.assertIn("teardown_hooks", result)

    def test_format_parse_config_level(self):
        """Test Format.parse() with config level"""
        body = {
            "name": "Test Config",
            "base_url": "http://api.test.com",
            "header": {"header": {"X-API-Key": "secret"}},
            "variables": {"variables": [{"env": "production"}]},
            "parameters": {"parameters": [{"user_id": "123"}]},
            "hooks": {"setup_hooks": ["init"], "teardown_hooks": ["cleanup"]}
        }
        
        format_obj = Format(body, level="config")
        format_obj.parse()
        
        result = format_obj.testcase
        self.assertEqual(result["name"], "Test Config")
        self.assertEqual(result["request"]["base_url"], "http://api.test.com")
        self.assertIn("headers", result["request"])
        self.assertIn("parameters", result)
        self.assertIn("variables", result)
        self.assertIn("setup_hooks", result)
        self.assertIn("teardown_hooks", result)

    def test_format_parse_minimal(self):
        """Test Format.parse() with minimal data"""
        body = {"name": "Minimal Test"}
        
        format_obj = Format(body, level="test")
        format_obj.parse()
        
        result = format_obj.testcase
        self.assertEqual(result["name"], "Minimal Test")
        self.assertNotIn("extract", result)
        self.assertNotIn("validate", result)
        self.assertNotIn("headers", result["request"])

    def test_format_parse_empty_json(self):
        """Test Format.parse() with empty json"""
        body = {
            "name": "Empty JSON Test",
            "request": {"json": {}}
        }
        
        format_obj = Format(body, level="test")
        format_obj.parse()
        
        result = format_obj.testcase
        self.assertIn("json", result["request"])
        self.assertEqual(result["request"]["json"], {})


@pytest.mark.django_db
class TestParse(TestCase):
    """Test Parse class"""

    def test_parse_init(self):
        """Test Parse initialization"""
        body = {
            "name": "Test Parse",
            "request": {"url": "/test", "method": "POST"},
            "variables": [{"var1": "value1"}],
            "setup_hooks": ["setup"],
            "teardown_hooks": ["teardown"],
            "desc": {"header": {}, "data": {}},
            "times": 5,
            "extract": [{"token": "$.token"}],
            "validate": [{"equals": ["status_code", 200]}]
        }
        
        parse_obj = Parse(body, level="test")
        
        self.assertEqual(parse_obj.name, "Test Parse")
        self.assertEqual(parse_obj._Parse__times, 5)

    def test_parse_get_type(self):
        """Test Parse.__get_type static method"""
        # Test string
        self.assertEqual(Parse._Parse__get_type("test"), (1, "test"))
        
        # Test int
        self.assertEqual(Parse._Parse__get_type(123), (2, "123"))
        
        # Test float
        self.assertEqual(Parse._Parse__get_type(3.14), (3, "3.14"))
        
        # Test bool
        self.assertEqual(Parse._Parse__get_type(True), (4, "True"))
        
        # Test list
        result = Parse._Parse__get_type([1, 2, 3])
        self.assertEqual(result[0], 5)
        self.assertEqual(json.loads(result[1]), [1, 2, 3])
        
        # Test dict
        result = Parse._Parse__get_type({"key": "value"})
        self.assertEqual(result[0], 6)
        self.assertEqual(json.loads(result[1]), {"key": "value"})
        
        # Test None
        self.assertEqual(Parse._Parse__get_type(None), (7, None))
        
        # Test string with $int
        self.assertEqual(Parse._Parse__get_type("$int(123)"), (2, "$int(123)"))

    def test_parse_http_test_level(self):
        """Test Parse.parse_http() with test level"""
        body = {
            "name": "Test API",
            "request": {
                "url": "/api/test",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "data": {"username": "test"},
                "params": {"page": "1"},
                "json": {"key": "value"}
            },
            "variables": [{"timeout": 30}],
            "setup_hooks": ["setup_test"],
            "teardown_hooks": ["teardown_test"],
            "desc": {
                "header": {"Content-Type": "Content type header"},
                "data": {"username": "Username field"},
                "params": {"page": "Page number"},
                "variables": {"timeout": "Request timeout"},
                "extract": {"token": "Auth token"}
            },
            "times": 3,
            "extract": [{"token": "$.response.token"}],
            "validate": [
                {"equals": ["status_code", 200, "Check status"]},
                {"contains": ["body", "success"]}
            ]
        }
        
        parse_obj = Parse(body, level="test")
        parse_obj.parse_http()
        
        result = parse_obj.testcase
        self.assertEqual(result["name"], "Test API")
        self.assertEqual(result["times"], 3)
        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["url"], "/api/test")
        
        # Check headers
        self.assertEqual(len(result["header"]), 1)
        self.assertEqual(result["header"][0]["key"], "Content-Type")
        
        # Check extract
        self.assertEqual(len(result["extract"]), 1)
        self.assertEqual(result["extract"][0]["key"], "token")
        
        # Check validate
        self.assertEqual(len(result["validate"]), 2)
        self.assertEqual(result["validate"][0]["comparator"], "equals")
        self.assertEqual(result["validate"][0]["desc"], "Check status")

    def test_parse_http_config_level(self):
        """Test Parse.parse_http() with config level"""
        body = {
            "name": "Test Config",
            "request": {
                "base_url": "http://test.com",
                "headers": {"Authorization": "Bearer token"}
            },
            "variables": [{"env": "test"}],
            "parameters": [{"user_id": "123", "group_id": "456"}],
            "desc": {
                "header": {"Authorization": "Auth header"},
                "variables": {"env": "Environment"},
                "parameters": {"user_id": "User ID", "group_id": "Group ID"}
            }
        }
        
        parse_obj = Parse(body, level="config")
        parse_obj.parse_http()
        
        result = parse_obj.testcase
        self.assertEqual(result["name"], "Test Config")
        self.assertEqual(result["base_url"], "http://test.com")
        
        # Check parameters
        self.assertEqual(len(result["parameters"]), 2)
        param_keys = [p["key"] for p in result["parameters"]]
        self.assertIn("user_id", param_keys)
        self.assertIn("group_id", param_keys)

    def test_parse_hooks_more_setup(self):
        """Test parse_hooks when setup hooks > teardown hooks"""
        body = {
            "name": "Test",
            "request": {"url": "/test", "method": "GET"},
            "setup_hooks": ["setup1", "setup2", "setup3"],
            "teardown_hooks": ["teardown1"],
            "desc": {}
        }
        
        parse_obj = Parse(body)
        parse_obj.parse_http()
        
        result = parse_obj.testcase
        self.assertEqual(len(result["hooks"]), 3)
        self.assertEqual(result["hooks"][0], {"setup": "setup1", "teardown": "teardown1"})
        self.assertEqual(result["hooks"][1], {"setup": "setup2", "teardown": ""})
        self.assertEqual(result["hooks"][2], {"setup": "setup3", "teardown": ""})

    def test_parse_hooks_more_teardown(self):
        """Test parse_hooks when teardown hooks > setup hooks"""
        body = {
            "name": "Test",
            "request": {"url": "/test", "method": "GET"},
            "setup_hooks": ["setup1"],
            "teardown_hooks": ["teardown1", "teardown2", "teardown3"],
            "desc": {}
        }
        
        parse_obj = Parse(body)
        parse_obj.parse_http()
        
        result = parse_obj.testcase
        self.assertEqual(len(result["hooks"]), 3)
        self.assertEqual(result["hooks"][0], {"setup": "setup1", "teardown": "teardown1"})
        self.assertEqual(result["hooks"][1], {"setup": "", "teardown": "teardown2"})
        self.assertEqual(result["hooks"][2], {"setup": "", "teardown": "teardown3"})


class TestUtilityFunctions(TestCase):
    """Test utility functions"""

    def test_format_json_valid(self):
        """Test format_json with valid JSON"""
        data = {"key": "value", "nested": {"inner": "data"}}
        result = format_json(data)
        
        # Should be formatted JSON string
        self.assertIn("key", result)
        self.assertIn("value", result)
        self.assertIn("    ", result)  # Check indentation

    def test_format_json_invalid(self):
        """Test format_json with invalid JSON"""
        # Circular reference
        data = {}
        data['self'] = data
        
        result = format_json(data)
        self.assertEqual(result, data)  # Should return original value

    def test_yapi_properties2json(self):
        """Test yapi_properties2json function"""
        properties = {
            "name": {
                "type": "string",
                "default": "test",
                "description": "Name field"
            },
            "age": {
                "type": "integer",
                "default": 25,
                "description": "Age field"
            },
            "items": {
                "type": "array",
                "description": "Array items"
            },
            "details": {
                "type": "object",
                "description": "Object details"
            }
        }
        
        req_json = {}
        variables = []
        desc = {}
        
        yapi_properties2json(properties, req_json, variables, desc)
        
        # Check non-array/object fields are processed
        self.assertEqual(req_json["name"], "$name")
        self.assertEqual(req_json["age"], "$age")
        self.assertNotIn("items", req_json)
        self.assertNotIn("details", req_json)
        
        # Check variables
        self.assertEqual(len(variables), 2)
        var_dict = {list(v.keys())[0]: list(v.values())[0] for v in variables}
        self.assertEqual(var_dict["name"], "test")
        self.assertEqual(var_dict["age"], 25)
        
        # Check descriptions
        self.assertEqual(desc["name"], "Name field")
        self.assertEqual(desc["age"], "Age field")

    @patch('os.getenv')
    @patch('fastrunner.models.Report.objects.last')
    def test_format_summary_to_ding_markdown(self, mock_last, mock_getenv):
        """Test format_summary_to_ding with markdown type"""
        mock_getenv.side_effect = lambda key, default: {
            "SERVER_IP": "192.168.1.1",
            "DJANGO_API_PORT": "8000"
        }.get(key, default)
        
        mock_report = Mock()
        mock_report.id = 123
        mock_last.return_value = mock_report
        
        summary = {
            "stat": {
                "testsRun": 10,
                "successes": 7,
                "failures": 2,
                "errors": 1
            },
            "time": {
                "start_at": 1609459200.0,
                "duration": 15.5
            },
            "details": [{
                "name": "Test Suite",
                "base_url": "http://test.example.com",
                "records": [
                    {
                        "name": "Failed Test",
                        "status": "failure",
                        "meta_data": {
                            "request": {"url": "/api/fail"},
                            "response": {
                                "json": {
                                    "info": {
                                        "message": "Invalid input",
                                        "error": "ValidationError"
                                    }
                                }
                            },
                            "validators": [
                                {"expect": 200, "check_value": 400}
                            ]
                        }
                    }
                ]
            }]
        }
        
        msg, fail_count = format_summary_to_ding("markdown", summary, "Test Report")
        
        self.assertEqual(fail_count, 2)
        self.assertIn("FasterRunner自动化测试报告", msg)
        self.assertIn("Test Report", msg)
        self.assertIn("15.50s", msg)
        self.assertIn("成功用例: 7个", msg)
        self.assertIn("失败用例: 2个", msg)
        self.assertIn("Failed Test", msg)
        self.assertIn("ValidationError", msg)

    def test_format_summary_to_ding_text(self):
        """Test format_summary_to_ding with text type"""
        summary = {
            "stat": {
                "testsRun": 5,
                "successes": 5,
                "failures": 0,
                "errors": 0
            },
            "time": {
                "start_at": 1609459200.0,
                "duration": 10.0
            },
            "details": [{
                "name": "Test Suite",
                "in_out": {
                    "in": {"report_url": "http://test.example.com"}
                },
                "records": []
            }]
        }
        
        msg, fail_count = format_summary_to_ding("text", summary)
        
        self.assertEqual(fail_count, 0)
        self.assertIn("自动化测试报告", msg)
        self.assertIn("环境:测试", msg)
        self.assertIn("通过率100.00%", msg)

    def test_format_summary_to_ding_no_report_url(self):
        """Test format_summary_to_ding without report_url"""
        summary = {
            "stat": {
                "testsRun": 1,
                "successes": 1,
                "failures": 0,
                "errors": 0
            },
            "time": {
                "start_at": 1609459200.0,
                "duration": 1.0
            },
            "details": [{
                "name": "Test",
                "base_url": "http://prod.example.com",
                "records": []
            }]
        }
        
        msg, fail_count = format_summary_to_ding("text", summary)
        
        self.assertIn("环境:生产", msg)

    def test_set_customized_variable(self):
        """Test set_customized_variable function"""
        api_info_template = {
            "request": {"json": {}},
            "variables": {"variables": [], "desc": {}}
        }
        
        items = {
            "type": "object",
            "properties": {
                "attributeName": {
                    "enum": ["name", "age", "email"],
                    "description": "Attribute name"
                },
                "rangeType": {
                    "enum": ["equals", "contains", "greater"],
                    "description": "Range type"
                }
            }
        }
        
        set_customized_variable(api_info_template, items)
        
        # Check conditions were set
        self.assertIn("conditions", api_info_template["request"]["json"])
        conditions = api_info_template["request"]["json"]["conditions"]
        self.assertEqual(conditions["attributeName"], "$name")
        self.assertEqual(conditions["rangeType"], "$rangeType")
        self.assertEqual(conditions["targetValue"], ["$name", "$age", "$email"])
        
        # Check orderBy was set
        self.assertIn("orderBy", api_info_template["request"]["json"])
        self.assertEqual(api_info_template["request"]["json"]["orderBy"][0]["rankType"], "DESC")
        
        # Check variables
        var_names = [list(v.keys())[0] for v in api_info_template["variables"]["variables"]]
        self.assertIn("name", var_names)
        self.assertIn("age", var_names)
        self.assertIn("email", var_names)
        self.assertIn("rangeType", var_names)

    def test_set_customized_variable_empty_enum(self):
        """Test set_customized_variable with empty enum"""
        api_info_template = {
            "request": {"json": {}},
            "variables": {"variables": [], "desc": {}}
        }
        
        items = {
            "type": "object",
            "properties": {
                "attributeName": {
                    "enum": [],
                    "description": "Empty enum"
                },
                "rangeType": {}
            }
        }
        
        set_customized_variable(api_info_template, items)
        
        # Should use empty string as default
        self.assertEqual(
            api_info_template["request"]["json"]["conditions"]["attributeName"],
            "$"
        )


@pytest.mark.django_db
class TestYapi(TestCase):
    """Test Yapi class"""

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
            tree=json.dumps([{"id": 1, "label": "Root", "children": [], "yapi_catid": 100}]),
            type=1
        )
        
        self.yapi = Yapi("http://yapi.test.com", "test_token", self.project.id)

    @patch('requests.get')
    def test_get_category_info_success(self, mock_get):
        """Test get_category_info with successful response"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "errcode": 0,
            "errmsg": "成功！",
            "data": [{
                "_id": 100,
                "name": "Test Category",
                "list": []
            }]
        }
        mock_get.return_value = mock_response
        
        result = self.yapi.get_category_info()
        
        self.assertEqual(result["errcode"], 0)
        self.assertIn("data", result)
        mock_get.assert_called_once_with(
            self.yapi.category_info_url,
            params={"token": "test_token"}
        )

    @patch('requests.get')
    def test_get_category_info_failure(self, mock_get):
        """Test get_category_info with exception"""
        mock_get.side_effect = Exception("Network error")
        
        result = self.yapi.get_category_info()
        
        self.assertEqual(result["errcode"], 1)
        self.assertIn("Network error", result["errmsg"])

    @patch.object(Yapi, 'get_category_info')
    def test_get_api_uptime_mapping(self, mock_get_info):
        """Test get_api_uptime_mapping"""
        mock_get_info.return_value = {
            "data": [{
                "list": [
                    {"_id": 1, "up_time": 1000},
                    {"_id": 2, "up_time": 2000}
                ]
            }]
        }
        
        result = self.yapi.get_api_uptime_mapping()
        
        self.assertEqual(result, {1: 1000, 2: 2000})

    @patch.object(Yapi, 'get_category_info')
    def test_get_category_id_name_mapping(self, mock_get_info):
        """Test get_category_id_name_mapping"""
        mock_get_info.return_value = {
            "errcode": 0,
            "data": [
                {"_id": 100, "name": "Category 1", "list": [{"_id": 1}]},
                {"_id": 200, "name": "Category 2", "list": []},  # Empty list, should be excluded
                {"_id": 300, "name": "Category 3", "list": [{"_id": 2}]}
            ]
        }
        
        result = self.yapi.get_category_id_name_mapping()
        
        self.assertEqual(result, {100: "Category 1", 300: "Category 3"})

    @patch('requests.get')
    def test_get_api_info_list(self, mock_get):
        """Test get_api_info_list"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "errcode": 0,
            "errmsg": "成功！",
            "data": {
                "list": [
                    {"_id": 1, "title": "API 1"},
                    {"_id": 2, "title": "API 2"}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        result = self.yapi.get_api_info_list()
        
        self.assertEqual(result["errcode"], 0)
        self.assertEqual(len(result["data"]["list"]), 2)

    @patch.object(Yapi, 'get_api_info_list')
    def test_get_api_ids(self, mock_get_list):
        """Test get_api_ids"""
        mock_get_list.return_value = {
            "data": {
                "list": [
                    {"_id": 1},
                    {"_id": 2},
                    {"_id": 3}
                ]
            }
        }
        
        result = self.yapi.get_api_ids()
        
        self.assertEqual(result, [1, 2, 3])

    @patch('requests.get')
    def test_get_batch_api_detail(self, mock_get):
        """Test get_batch_api_detail"""
        def mock_api_response(url):
            api_id = url.split("id=")[1]
            response = Mock()
            response.json.return_value = {
                "data": {
                    "_id": int(api_id),
                    "title": f"API {api_id}"
                }
            }
            return response
        
        mock_get.side_effect = lambda url, **kwargs: mock_api_response(url)
        
        result = self.yapi.get_batch_api_detail([1, 2, 3])
        
        self.assertEqual(len(result), 3)
        titles = [api["title"] for api in result]
        self.assertIn("API 1", titles)
        self.assertIn("API 2", titles)
        self.assertIn("API 3", titles)

    def test_get_variable_default_value(self):
        """Test get_variable_default_value"""
        # Test integer
        self.assertEqual(
            self.yapi.get_variable_default_value("integer", {"default": 42}),
            42
        )
        
        # Test number
        self.assertEqual(
            self.yapi.get_variable_default_value("number", {"default": 3.14}),
            3.14
        )
        
        # Test bigdecimal
        self.assertEqual(
            self.yapi.get_variable_default_value("bigdecimal", {"default": 999.99}),
            999.99
        )
        
        # Test date
        result = self.yapi.get_variable_default_value("date", {})
        self.assertIn("-", result)  # Date format check
        
        # Test string
        self.assertEqual(
            self.yapi.get_variable_default_value("string", {}),
            ""
        )
        
        # Test unknown type
        self.assertEqual(
            self.yapi.get_variable_default_value("unknown", {}),
            ""
        )
        
        # Test non-dict input
        self.assertEqual(
            self.yapi.get_variable_default_value("integer", "not a dict"),
            ""
        )

    @patch.object(Yapi, 'get_category_id_name_mapping')
    def test_create_relation_id(self, mock_get_mapping):
        """Test create_relation_id"""
        mock_get_mapping.return_value = {
            100: "Existing Category",
            200: "New Category 1",
            300: "New Category 2"
        }
        
        self.yapi.create_relation_id(self.project.id)
        
        # Check tree was updated
        relation = models.Relation.objects.get(project=self.project, type=1)
        tree = json.loads(relation.tree)
        
        # Should have added new categories
        self.assertEqual(len(tree), 3)  # 1 existing + 2 new
        cat_ids = [node.get("yapi_catid") for node in tree]
        self.assertIn(200, cat_ids)
        self.assertIn(300, cat_ids)

    def test_create_relation_id_none_mapping(self):
        """Test create_relation_id with None mapping"""
        with patch.object(Yapi, 'get_category_id_name_mapping') as mock_get:
            mock_get.return_value = None
            
            # Should not raise exception
            self.yapi.create_relation_id(self.project.id)

    def test_yapi2faster_basic(self):
        """Test yapi2faster basic conversion"""
        source_api = {
            "_id": 123,
            "title": "Test API",
            "path": "/api/{id}/test",
            "method": "POST",
            "catid": 100,
            "add_time": 1609459200,
            "up_time": 1609545600,
            "username": "testuser",
            "req_body_type": "raw",
            "req_query": [
                {"name": "page", "desc": "Page number"}
            ],
            "req_params": [
                {"name": "namespace", "desc": "Namespace", "example": "test"}
            ]
        }
        
        result = self.yapi.yapi2faster(source_api)
        
        self.assertEqual(result["name"], "Test API")
        self.assertEqual(result["url"], "/api/$id/test")  # {id} -> $id
        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["yapi_catid"], 100)
        self.assertEqual(result["yapi_id"], 123)
        
        # Check params
        self.assertIn("page", result["request"]["params"]["params"])
        
        # Check variables
        var_names = [list(v.keys())[0] for v in result["variables"]["variables"]]
        self.assertIn("page", var_names)
        self.assertIn("namespace", var_names)

    @patch('json.loads')
    @patch('json5.loads')
    def test_yapi2faster_json_body(self, mock_json5, mock_json):
        """Test yapi2faster with JSON body"""
        mock_json.side_effect = json.JSONDecodeError("error", "", 0)
        mock_json5.return_value = {
            "properties": {
                "name": {"type": "string", "description": "Name field"},
                "age": {"type": "integer", "default": 25},
                "items": {"type": "array", "items": {"type": "string"}},
                "details": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "Address"}
                    }
                },
                "nullable_field": {
                    "anyOf": [
                        {"type": "string", "description": "String value"},
                        {"type": "null"}
                    ]
                }
            }
        }
        
        source_api = {
            "_id": 123,
            "title": "JSON API",
            "path": "/api/test",
            "method": "POST",
            "catid": 100,
            "req_body_type": "json",
            "req_body_other": '{"test": "data"}'  # Will fail regular JSON
        }
        
        result = self.yapi.yapi2faster(source_api)
        
        # Check ordinary fields
        self.assertEqual(result["request"]["json"]["name"], "$name")
        self.assertEqual(result["request"]["json"]["age"], "$age")
        
        # Check nested object field
        self.assertEqual(result["request"]["json"]["address"], "$address")
        
        # Check anyOf handling
        self.assertEqual(result["request"]["json"]["nullable_field"], "$nullable_field")

    def test_yapi2faster_conditions_array(self):
        """Test yapi2faster with conditions array"""
        source_api = {
            "_id": 123,
            "title": "Conditions API",
            "path": "/api/search",
            "method": "POST",
            "catid": 100,
            "req_body_type": "json",
            "req_body_other": json.dumps({
                "properties": {
                    "conditions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "attributeName": {"enum": ["name", "age"]},
                                "rangeType": {"enum": ["equals", "contains"]}
                            }
                        }
                    }
                }
            })
        }
        
        result = self.yapi.yapi2faster(source_api)
        
        # Check conditions were handled
        self.assertIn("conditions", result["request"]["json"])

    def test_yapi2faster_unhandled_field_type(self):
        """Test yapi2faster with unhandled field type"""
        source_api = {
            "_id": 123,
            "title": "Unknown Type API",
            "path": "/api/test",
            "method": "GET",
            "catid": 100,
            "req_body_type": "json",
            "req_body_other": json.dumps({
                "properties": {
                    "field": {"no_type": "field"}  # Missing type
                }
            })
        }
        
        with patch('fastrunner.utils.parser.logger') as mock_logger:
            result = self.yapi.yapi2faster(source_api)
            
            # Should log error about unknown type
            mock_logger.error.assert_called()

    def test_yapi2faster_long_title(self):
        """Test yapi2faster with long title"""
        source_api = {
            "_id": 123,
            "title": "A" * 200,  # Very long title
            "path": "/api/test",
            "method": "GET",
            "catid": 100
        }
        
        result = self.yapi.yapi2faster(source_api)
        
        # Title should be truncated to 100 chars
        self.assertEqual(len(result["name"]), 100)

    def test_set_ordinary_variable(self):
        """Test set_ordinary_variable method"""
        api_info_template = {
            "request": {"json": {}},
            "variables": {"variables": [], "desc": {}}
        }
        
        self.yapi.set_ordinary_variable(
            api_info_template,
            "test_field",
            "string",
            {"description": "Test description"}
        )
        
        self.assertEqual(api_info_template["request"]["json"]["test_field"], "$test_field")
        self.assertEqual(len(api_info_template["variables"]["variables"]), 1)
        self.assertEqual(api_info_template["variables"]["desc"]["test_field"], "Test description")

    @patch.object(Format, 'parse')
    def test_get_parsed_apis(self, mock_parse):
        """Test get_parsed_apis"""
        api_info = [
            {
                "_id": 1,
                "title": "API 1",
                "path": "/api/1",
                "method": "GET",
                "catid": 100,
                "ypai_add_time": 1000,
                "ypai_up_time": 2000,
                "ypai_username": "user1"
            },
            "not a dict"  # Should be skipped
        ]
        
        # Mock yapi2faster
        with patch.object(self.yapi, 'yapi2faster') as mock_y2f:
            mock_y2f.return_value = {
                "name": "API 1",
                "url": "/api/1",
                "method": "GET",
                "yapi_catid": 100,
                "yapi_id": 1,
                "ypai_add_time": 1000,
                "ypai_up_time": 2000,
                "ypai_username": "user1"
            }
            
            result = self.yapi.get_parsed_apis(api_info)
            
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], models.API)
            self.assertEqual(result[0].name, "API 1")
            self.assertEqual(result[0].creator, "yapi")

    def test_merge_api_new_apis(self):
        """Test merge_api with new APIs"""
        # Create existing API
        existing_api = models.API(
            name="Existing API",
            project=self.project,
            yapi_id=100,
            ypai_up_time="1000"
        )
        
        # Create parsed APIs
        new_api1 = models.API(
            name="New API 1",
            project=self.project,
            yapi_id=200,
            ypai_up_time="2000"
        )
        new_api2 = models.API(
            name="New API 2",
            project=self.project,
            yapi_id=300,
            ypai_up_time="3000"
        )
        
        update_apis, new_apis = self.yapi.merge_api(
            [new_api1, new_api2],
            [existing_api]
        )
        
        self.assertEqual(len(new_apis), 2)
        self.assertEqual(len(update_apis), 0)

    def test_merge_api_update_apis(self):
        """Test merge_api with APIs to update"""
        # Create existing API
        existing_api = models.API(
            name="Old Name",
            project=self.project,
            yapi_id=100,
            ypai_up_time="1000",
            method="GET",
            url="/old",
            body="{}"
        )
        
        # Create parsed API with same yapi_id but newer up_time
        updated_api = models.API(
            name="New Name",
            project=self.project,
            yapi_id=100,
            ypai_up_time="2000",
            method="POST",
            url="/new",
            body='{"updated": true}'
        )
        
        update_apis, new_apis = self.yapi.merge_api(
            [updated_api],
            [existing_api]
        )
        
        self.assertEqual(len(new_apis), 0)
        self.assertEqual(len(update_apis), 1)
        self.assertEqual(update_apis[0].name, "New Name")
        self.assertEqual(update_apis[0].method, "POST")

    def test_get_create_or_update_apis(self):
        """Test get_create_or_update_apis"""
        imported_mapping = {
            100: "1000",  # Existing API
            200: "2000"   # Existing API
        }
        
        with patch.object(self.yapi, 'get_api_uptime_mapping') as mock_mapping:
            mock_mapping.return_value = {
                100: 1000,    # Same up_time, no update
                200: 3000,    # Newer up_time, needs update
                300: 4000     # New API
            }
            
            create_ids, update_ids = self.yapi.get_create_or_update_apis(imported_mapping)
            
            self.assertEqual(create_ids, [300])
            self.assertEqual(update_ids, [200])