"""Test for fastrunner.utils.loader module"""
import json
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.test import TestCase

from fastrunner.models import API, Case, CaseStep, Config, Project, Report, ReportDetail
from fastrunner.utils.loader import (
    FileLoader,
    debug_api,
    debug_suite,
    load_debugtalk,
    load_test,
    parse_summary,
    parse_tests,
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

    def test_load_test(self):
        """Test load_test function"""
        # Create test case with steps
        case = Case.objects.create(
            name="Load Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        CaseStep.objects.create(
            case=case,
            name="Step 1",
            step=1,
            body=json.dumps({
                "name": "Step 1",
                "request": {"url": "/test", "method": "GET"}
            }),
            url="/test",
            method="GET"
        )
        
        result = load_test(case.id, project=self.project.id)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

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

    def test_parse_tests(self):
        """Test parse_tests function"""
        testcases = [
            {
                "name": "Test 1",
                "request": {
                    "url": "/api/test",
                    "method": "GET"
                }
            }
        ]
        
        debugtalk = "def helper(): return 'test'"
        
        result = parse_tests(
            testcases, 
            debugtalk,
            name="Test Suite",
            config=None,
            project=self.project.id
        )
        
        self.assertIsNotNone(result)

    def test_parse_summary(self):
        """Test parse_summary function"""
        summary_raw = {
            "success": True,
            "stat": {
                "testcases": {"total": 10, "success": 8, "fail": 2}
            },
            "time": {
                "start_at": datetime.now().isoformat(),
                "duration": 60.5
            },
            "details": [
                {
                    "name": "test1",
                    "success": True,
                    "stat": {"total": 5, "successes": 5, "failures": 0}
                }
            ]
        }
        
        result = parse_summary(summary_raw)
        
        self.assertIsInstance(result, str)
        parsed = json.loads(result)
        self.assertIn("stat", parsed)
        self.assertIn("time", parsed)

    def test_file_loader(self):
        """Test FileLoader class"""
        loader = FileLoader("test_path")
        
        # Test extract_field with mock response
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

