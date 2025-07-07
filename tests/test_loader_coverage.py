"""Test for fastrunner.utils.loader module"""
import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.test import TestCase

from fastrunner.models import API, Case, CaseStep, Config, Project, Report, ReportDetail
from fastrunner.utils.loader import (
    TestCaseLoader,
    debug_api,
    debug_suite,
    get_unique_testcase,
    load_debugtalk,
    load_test_dependencies,
    save_api_casestep,
    save_last_run,
    save_summary,
)


@pytest.mark.django_db
class TestLoaderFunctions(TestCase):
    """Test loader utility functions"""

    def setUp(self):
        self.project = Project.objects.create(
            name="Loader Test Project",
            desc="Test",
            responsible="test"
        )
        
        self.config = Config.objects.create(
            name="Test Config",
            project=self.project,
            body=json.dumps({
                "name": "Test Config",
                "request": {
                    "base_url": "http://localhost:8000"
                }
            })
        )
        
        self.api = API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/api/test",
            body=json.dumps({
                "name": "Test API",
                "request": {
                    "url": "/api/test",
                    "method": "GET",
                    "headers": {"Content-Type": "application/json"}
                },
                "validate": [
                    {"eq": ["status_code", 200]}
                ]
            }),
            relation=1
        )

    @patch('fastrunner.utils.loader.build_url')
    @patch('fastrunner.utils.loader.RunByHttpRunner')
    def test_debug_api_success(self, mock_runner_class, mock_build_url):
        """Test debug_api function with successful run"""
        # Setup mocks
        mock_build_url.return_value = "http://localhost:8000/api/test"
        mock_runner = MagicMock()
        mock_runner.run.return_value = {
            "success": True,
            "stat": {
                "testcases": {"total": 1, "success": 1, "fail": 0}
            },
            "time": {
                "start_at": datetime.now().isoformat(),
                "duration": 0.5
            }
        }
        mock_runner_class.return_value = mock_runner
        
        # Call function
        result = debug_api(
            api=self.api.id,
            project=self.project.id,
            config=self.config.id,
            save=False
        )
        
        # Verify
        self.assertTrue(result["success"])
        mock_runner.run.assert_called_once()

    @patch('fastrunner.utils.loader.RunByHttpRunner')
    def test_debug_api_with_save(self, mock_runner_class):
        """Test debug_api with save=True"""
        mock_runner = MagicMock()
        mock_runner.run.return_value = {
            "success": True,
            "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
        }
        mock_runner_class.return_value = mock_runner
        
        with patch('fastrunner.utils.loader.save_summary') as mock_save:
            mock_save.return_value = 1
            
            result = debug_api(
                api=self.api.id,
                project=self.project.id,
                name="Test Run",
                save=True
            )
            
            mock_save.assert_called_once()

    @patch('fastrunner.models.CaseStep.objects.filter')
    @patch('fastrunner.utils.loader.RunByHttpRunner')
    def test_debug_suite(self, mock_runner_class, mock_filter):
        """Test debug_suite function"""
        # Create test case
        case = Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Mock case steps
        mock_step = MagicMock()
        mock_step.body = json.dumps({
            "name": "Test Step",
            "request": {
                "url": "/api/test",
                "method": "GET"
            }
        })
        mock_filter.return_value.order_by.return_value.values.return_value = [
            {"body": mock_step.body}
        ]
        
        # Mock runner
        mock_runner = MagicMock()
        mock_runner.run.return_value = {
            "success": True,
            "stat": {"testcases": {"total": 1, "success": 1, "fail": 0}}
        }
        mock_runner_class.return_value = mock_runner
        
        # Call function
        result, _ = debug_suite(
            suite=[case.id],
            project=self.project.id,
            obj=[{"name": case.name, "id": case.id}],
            config=[self.config.id],
            save=False
        )
        
        self.assertTrue(result["success"])

    def test_get_unique_testcase(self):
        """Test get_unique_testcase function"""
        testcases = [
            {"name": "test1", "request": {"url": "/api/1"}},
            {"name": "test2", "request": {"url": "/api/2"}},
            {"name": "test1", "request": {"url": "/api/1"}},  # Duplicate
            {"name": "test3", "request": {"url": "/api/3"}}
        ]
        
        unique = get_unique_testcase(testcases)
        
        self.assertEqual(len(unique), 3)
        names = [tc["name"] for tc in unique]
        self.assertEqual(names, ["test1", "test2", "test3"])

    @patch('builtins.open', create=True)
    @patch('os.path.exists')
    def test_load_debugtalk(self, mock_exists, mock_open):
        """Test load_debugtalk function"""
        # Test when file exists
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = "def custom_func(): pass"
        
        result = load_debugtalk("/test/path")
        self.assertEqual(result, "def custom_func(): pass")
        
        # Test when file doesn't exist
        mock_exists.return_value = False
        result = load_debugtalk("/test/path")
        self.assertEqual(result, "")

    def test_load_test_dependencies(self):
        """Test load_test_dependencies function"""
        # Create dependency case
        dep_case = Case.objects.create(
            name="Dependency Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create case step with dependency
        CaseStep.objects.create(
            case=dep_case,
            name="Dep Step",
            step=1,
            body=json.dumps({
                "name": "Dep Step",
                "request": {"url": "/dep", "method": "GET"}
            }),
            url="/dep",
            method="GET"
        )
        
        # Create main testcase with dependency
        testcase = {
            "name": "Main Test",
            "testcase_def": f"${{debugtalk.CaseStep({dep_case.id})}}",
            "request": {"url": "/main", "method": "POST"}
        }
        
        with patch('fastrunner.models.CaseStep.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value.values.return_value = [
                {"body": json.dumps({"name": "Dep Step", "request": {"url": "/dep"}})}
            ]
            
            result = load_test_dependencies(testcase)
            
            # Should have both dependency and main test
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Dep Step")
            self.assertEqual(result[1]["name"], "Main Test")

    def test_save_api_casestep(self):
        """Test save_api_casestep function"""
        api_list = ["Test API 1", "Test API 2"]
        config = {"name": "Config", "request": {"base_url": "http://test.com"}}
        
        with patch('fastrunner.models.API.objects.filter') as mock_filter:
            # Mock API lookup
            mock_api = MagicMock()
            mock_api.body = json.dumps({
                "name": "Test API",
                "request": {"url": "/test", "method": "GET"}
            })
            mock_filter.return_value.values.return_value.first.return_value = {
                "body": mock_api.body
            }
            
            result = save_api_casestep(api_list, config)
            
            # Should have config + 2 APIs
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0], config)

    @patch('fastrunner.models.Report.objects.filter')
    def test_save_last_run(self, mock_filter):
        """Test save_last_run function"""
        # Mock report
        mock_report = MagicMock()
        mock_report.summary = json.dumps({
            "success": True,
            "time": {"start_at": "2023-01-01T10:00:00"},
            "stat": {"testcases": {"total": 10, "success": 8, "fail": 2}}
        })
        mock_filter.return_value.last.return_value = mock_report
        
        result = save_last_run(1, "api")
        
        self.assertIn("last_run_time", result)
        self.assertIn("last_run_status", result)
        self.assertEqual(result["last_run_status"], 1)  # Has failures
        
        # Test with no report
        mock_filter.return_value.last.return_value = None
        result = save_last_run(1, "api")
        self.assertEqual(result["last_run_time"], "")
        self.assertEqual(result["last_run_status"], -1)

    def test_testcase_loader_extract_field(self):
        """Test TestCaseLoader extract_field method"""
        loader = TestCaseLoader("")
        
        testcase = {
            "name": "Test",
            "extract": [
                {"token": "content.token"},
                {"user_id": "content.user.id"}
            ]
        }
        
        # Mock response
        response = Mock()
        response.status_code = 200
        response.content = b'{"content": {"token": "abc123", "user": {"id": 456}}}'
        response.elapsed = Mock(total_seconds=Mock(return_value=0.5))
        response.headers = {"Content-Type": "application/json"}
        
        with patch('json.loads') as mock_json:
            mock_json.return_value = {
                "content": {
                    "token": "abc123",
                    "user": {"id": 456}
                }
            }
            
            result = loader.extract_field(testcase, response)
            
            self.assertEqual(result["token"], "abc123")
            self.assertEqual(result["user_id"], 456)

    def test_testcase_loader_parser(self):
        """Test TestCaseLoader parser method"""
        loader = TestCaseLoader("")
        
        # Test with override config
        config = {"name": "Override", "request": {"base_url": "http://override.com"}}
        testcases = [
            {"name": "Config", "request": {"base_url": "http://old.com"}},
            {"name": "Test1", "request": {"url": "/test1"}},
            {"name": "Test2", "request": {"url": "/test2"}}
        ]
        
        result = loader.parser(testcases, level="test", config=config)
        
        # First should be override config
        self.assertEqual(result[0]["name"], "Override")
        self.assertEqual(len(result), 3)
        
        # Test without override
        result = loader.parser(testcases, level="test")
        self.assertEqual(result[0]["name"], "Config")
        self.assertEqual(len(result), 3)