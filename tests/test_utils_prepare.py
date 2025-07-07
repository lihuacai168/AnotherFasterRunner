"""Comprehensive tests for fastrunner.utils.prepare module to achieve 100% coverage"""
import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from django.test import TestCase

from fastrunner import models
from fastrunner.utils import prepare
from fastuser.models import MyUser


@pytest.mark.django_db
class TestPrepareUtils(TestCase):
    """Test all functions in prepare module"""

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

    def test_get_counter_with_pk(self):
        """Test get_counter with project pk"""
        # Create test data
        models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        
        count = prepare.get_counter(models.API, pk=self.project.id)
        self.assertEqual(count, 1)

    def test_get_counter_without_pk(self):
        """Test get_counter without project pk"""
        # Create test data
        models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        
        count = prepare.get_counter(models.API)
        self.assertEqual(count, 1)

    def test_report_status_count(self):
        """Test report_status_count function"""
        # Create reports with different statuses
        models.Report.objects.create(
            project=self.project,
            name="Failed Report",
            type=1,
            status=0,
            creator="test"
        )
        models.Report.objects.create(
            project=self.project,
            name="Success Report",
            type=1,
            status=1,
            creator="test"
        )
        
        fail_count, success_count = prepare.report_status_count(self.project.id)
        self.assertEqual(fail_count, 1)
        self.assertEqual(success_count, 1)

    @patch('fastrunner.utils.prepare.get_day')
    @patch('fastrunner.utils.prepare.get_week')
    @patch('fastrunner.utils.prepare.get_month')
    def test_get_recent_date(self, mock_month, mock_week, mock_day):
        """Test get_recent_date for different date types"""
        # Mock return values
        mock_day.side_effect = lambda n: f"2023-01-{10+n}"
        mock_week.side_effect = lambda n: f"2023-W{10+n}"
        mock_month.side_effect = lambda n: f"2023-{10+n}"
        
        # Test day
        result = prepare.get_recent_date("day")
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], "2023-01-5")
        
        # Test week
        result = prepare.get_recent_date("week")
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], "2023-W5")
        
        # Test month
        result = prepare.get_recent_date("month")
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], "2023-5")

    def test_list2dict(self):
        """Test list2dict conversion"""
        arr = [
            {"create_time": "2023-01-01", "counts": 10},
            {"create_time": "2023-01-02", "counts": 20}
        ]
        result = prepare.list2dict(arr)
        expected = {"2023-01-01": 10, "2023-01-02": 20}
        self.assertEqual(result, expected)

    @patch('fastrunner.utils.prepare.get_recent_date')
    def test_complete_list(self, mock_recent_date):
        """Test complete_list function"""
        mock_recent_date.return_value = ["2023-01-01", "2023-01-02", "2023-01-03"]
        arr = [{"create_time": "2023-01-01", "counts": 10}]
        
        result = prepare.complete_list(arr, "day")
        self.assertEqual(result, [10, 0, 0])

    def test_get_sql_dateformat(self):
        """Test get_sql_dateformat for different date types"""
        self.assertEqual(prepare.get_sql_dateformat("week"), "YEARWEEK(create_time,'%Y-%m-%d')")
        self.assertEqual(prepare.get_sql_dateformat("month"), "DATE_FORMAT(create_time,'%Y%m')")
        self.assertEqual(prepare.get_sql_dateformat("day"), "DATE_FORMAT(create_time,'%Y-%m-%d')")

    def test_get_project_api_cover(self):
        """Test get_project_api_cover function"""
        # Create case and case steps
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=2
        )
        models.CaseStep.objects.create(
            case=case,
            name="Step 1",
            url="/api/test",
            method="GET",
            body="{}",
            step=0
        )
        models.CaseStep.objects.create(
            case=case,
            name="Step 2",
            url="/api/test",
            method="POST",
            body="{}",
            step=1
        )
        # Add a config step that should be excluded
        models.CaseStep.objects.create(
            case=case,
            name="Config",
            url="",
            method="config",
            body="{}",
            step=2
        )
        
        result = prepare.get_project_api_cover(self.project.id)
        self.assertEqual(result['url_method__count'], 2)

    def test_get_project_apis(self):
        """Test get_project_apis function"""
        # Create APIs with different creators
        models.API.objects.create(
            name="User API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1,
            creator="user"
        )
        models.API.objects.create(
            name="YAPI Import",
            project=self.project,
            method="GET",
            url="/test2",
            body="{}",
            relation=1,
            creator="yapi"
        )
        # Create a deleted API (should be excluded)
        models.API.objects.create(
            name="Deleted API",
            project=self.project,
            method="GET",
            url="/test3",
            body="{}",
            relation=1,
            delete=1
        )
        
        keys, values = prepare.get_project_apis(self.project.id)
        self.assertEqual(keys, ['用户创建', 'yapi导入'])
        self.assertEqual(values, [1, 1])

    def test_get_project_apis_no_project(self):
        """Test get_project_apis without project filter"""
        keys, values = prepare.get_project_apis(None)
        self.assertEqual(keys, ['用户创建', 'yapi导入'])

    @patch('fastrunner.utils.prepare.complete_list')
    def test_aggregate_apis_bydate(self, mock_complete):
        """Test aggregate_apis_bydate function"""
        mock_complete.return_value = [1, 2, 3, 4, 5, 6]
        
        # Test non-yapi
        result = prepare.aggregate_apis_bydate("day", is_yapi=False)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])
        
        # Test yapi
        result = prepare.aggregate_apis_bydate("day", is_yapi=True)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_aggregate_case_by_tag(self):
        """Test aggregate_case_by_tag function"""
        # Create cases with different tags
        models.Case.objects.create(
            name="Smoke Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        models.Case.objects.create(
            name="Integration Case",
            project=self.project,
            tag=2,
            relation=1,
            length=1
        )
        models.Case.objects.create(
            name="Monitor Case",
            project=self.project,
            tag=3,
            relation=1,
            length=1
        )
        models.Case.objects.create(
            name="Core Case",
            project=self.project,
            tag=4,
            relation=1,
            length=1
        )
        
        keys, values = prepare.aggregate_case_by_tag(self.project.id)
        self.assertEqual(keys, ['冒烟用例', '集成用例', '监控脚本', '核心用例'])
        self.assertEqual(values, [1, 1, 1, 1])

    def test_aggregate_case_by_tag_no_project(self):
        """Test aggregate_case_by_tag without project filter"""
        keys, values = prepare.aggregate_case_by_tag(None)
        self.assertEqual(len(keys), 4)

    def test_aggregate_reports_by_type(self):
        """Test aggregate_reports_by_type function"""
        # Create reports with different types
        for report_type in [1, 2, 3, 4]:
            models.Report.objects.create(
                project=self.project,
                name=f"Report Type {report_type}",
                type=report_type,
                status=1,
                creator="test"
            )
        
        keys, values = prepare.aggregate_reports_by_type(self.project.id)
        self.assertEqual(keys, ['调试', '异步', '定时', '部署'])
        self.assertEqual(values, [1, 1, 1, 1])

    def test_aggregate_reports_by_type_no_project(self):
        """Test aggregate_reports_by_type without project filter"""
        keys, values = prepare.aggregate_reports_by_type(None)
        self.assertEqual(len(keys), 4)

    def test_aggregate_reports_by_status(self):
        """Test aggregate_reports_by_status function"""
        # Create reports with different statuses
        models.Report.objects.create(
            project=self.project,
            name="Failed Report",
            type=1,
            status=0,
            creator="test"
        )
        models.Report.objects.create(
            project=self.project,
            name="Success Report",
            type=1,
            status=1,
            creator="test"
        )
        
        keys, values = prepare.aggregate_reports_by_status(self.project.id)
        self.assertEqual(keys, ['失败', '成功'])
        self.assertEqual(values, [1, 1])

    def test_aggregate_reports_by_status_no_project(self):
        """Test aggregate_reports_by_status without project filter"""
        keys, values = prepare.aggregate_reports_by_status(None)
        self.assertEqual(len(keys), 2)

    @patch('fastrunner.utils.prepare.complete_list')
    def test_aggregate_reports_or_case_bydate(self, mock_complete):
        """Test aggregate_reports_or_case_bydate function"""
        mock_complete.return_value = [1, 2, 3, 4, 5, 6]
        
        result = prepare.aggregate_reports_or_case_bydate("day", models.Report)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    @patch('fastrunner.utils.prepare.get_day')
    def test_get_daily_count(self, mock_get_day):
        """Test get_daily_count function"""
        # Mock get_day to return predictable dates
        mock_get_day.side_effect = lambda n: f"2023-01-{10+n}" if n < 0 else "2023-01-10"
        
        # Create test data
        api = models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        # Set create_time manually
        api.create_time = datetime(2023, 1, 9)
        api.save()
        
        result = prepare.get_daily_count(self.project.id, "api", -2, 0)
        self.assertIn("days", result)
        self.assertIn("count", result)
        self.assertEqual(len(result["days"]), 2)

    @patch('fastrunner.utils.prepare.get_daily_count')
    def test_get_project_daily_create(self, mock_daily_count):
        """Test get_project_daily_create function"""
        mock_daily_count.return_value = {"days": ["01-01"], "count": [1]}
        
        result = prepare.get_project_daily_create(self.project.id)
        self.assertIn("api", result)
        self.assertIn("case", result)
        self.assertIn("report", result)

    @patch('fastrunner.utils.prepare.get_project_apis')
    @patch('fastrunner.utils.prepare.aggregate_case_by_tag')
    @patch('fastrunner.utils.prepare.aggregate_reports_by_type')
    @patch('fastrunner.utils.prepare.get_project_daily_create')
    def test_get_project_detail_v2(self, mock_daily, mock_report, mock_case, mock_api):
        """Test get_project_detail_v2 function"""
        mock_api.return_value = (["用户创建", "yapi导入"], [10, 5])
        mock_case.return_value = (["冒烟用例", "集成用例"], [20, 15])
        mock_report.return_value = (["调试", "异步"], [30, 25])
        mock_daily.return_value = {"api": {}, "case": {}, "report": {}}
        
        result = prepare.get_project_detail_v2(self.project.id)
        self.assertIn("api_count_by_create_type", result)
        self.assertIn("case_count_by_tag", result)
        self.assertIn("report_count_by_type", result)
        self.assertIn("daily_create_count", result)

    @patch('requests.post')
    def test_get_jira_core_case_cover_rate_no_config(self, mock_post):
        """Test get_jira_core_case_cover_rate with no jira config"""
        result = prepare.get_jira_core_case_cover_rate(self.project.id)
        self.assertEqual(result["jira_core_case_count"], 0)
        self.assertEqual(result["core_case_count"], 0)
        self.assertEqual(result["core_case_cover_rate"], "0.00")
        mock_post.assert_not_called()

    @patch('requests.post')
    def test_get_jira_core_case_cover_rate_with_config(self, mock_post):
        """Test get_jira_core_case_cover_rate with jira config"""
        # Set jira config
        self.project.jira_bearer_token = "test_token"
        self.project.jira_project_key = "TEST"
        self.project.save()
        
        # Mock jira response
        mock_response = Mock()
        mock_response.json.return_value = {
            "issues": [
                {
                    "fields": {
                        "customfield_11400": {"value": "是"}
                    }
                },
                {
                    "fields": {
                        "customfield_11400": {"value": "否"}
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Create core case
        models.Case.objects.create(
            name="Core Case",
            project=self.project,
            tag=4,
            relation=1,
            length=1
        )
        
        result = prepare.get_jira_core_case_cover_rate(self.project.id)
        self.assertEqual(result["jira_core_case_count"], 1)
        self.assertEqual(result["core_case_count"], 1)
        self.assertEqual(result["core_case_cover_rate"], "100.00")

    @patch('requests.post')
    def test_get_jira_core_case_cover_rate_error(self, mock_post):
        """Test get_jira_core_case_cover_rate with error response"""
        self.project.jira_bearer_token = "test_token"
        self.project.jira_project_key = "TEST"
        self.project.save()
        
        # Mock error response
        mock_response = Mock()
        mock_response.json.return_value = {
            "errorMessages": ["Authentication failed"]
        }
        mock_post.return_value = mock_response
        
        result = prepare.get_jira_core_case_cover_rate(self.project.id)
        self.assertEqual(result["jira_core_case_count"], 0)

    @patch('requests.post')
    def test_get_jira_core_case_cover_rate_exception(self, mock_post):
        """Test get_jira_core_case_cover_rate with exception"""
        self.project.jira_bearer_token = "test_token"
        self.project.jira_project_key = "TEST"
        self.project.save()
        
        mock_post.side_effect = Exception("Network error")
        
        result = prepare.get_jira_core_case_cover_rate(self.project.id)
        self.assertEqual(result["jira_core_case_count"], 0)

    @patch('django_celery_beat.models.PeriodicTask.objects.filter')
    def test_get_project_detail(self, mock_periodic_filter):
        """Test get_project_detail function"""
        # Create test data
        models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=5
        )
        models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body="{}"
        )
        models.Variables.objects.create(
            key="test_var",
            value="test_value",
            project=self.project
        )
        models.Report.objects.create(
            project=self.project,
            name="Test Report",
            type=1,
            status=1,
            creator="test"
        )
        models.HostIP.objects.create(
            name="Test Host",
            host="http://test.com",
            project=self.project
        )
        
        # Mock periodic task queryset
        mock_task_qs = Mock()
        mock_task_qs.count.return_value = 1
        mock_task_qs.filter.return_value.values.return_value = [{"args": "[1]"}]
        mock_periodic_filter.return_value = mock_task_qs
        
        result = prepare.get_project_detail(self.project.id)
        self.assertEqual(result["api_count"], 1)
        self.assertEqual(result["case_count"], 1)
        self.assertEqual(result["config_count"], 1)
        self.assertEqual(result["variables_count"], 1)
        self.assertEqual(result["report_count"], 1)
        self.assertEqual(result["host_count"], 1)
        self.assertEqual(result["task_count"], 1)

    def test_project_init(self):
        """Test project_init function"""
        new_project = models.Project.objects.create(
            name="New Project",
            desc="Test",
            responsible="testuser"
        )
        
        prepare.project_init(new_project)
        
        # Check if debugtalk was created
        self.assertTrue(models.Debugtalk.objects.filter(project=new_project).exists())

    @patch('django_celery_beat.models.PeriodicTask.objects.filter')
    def test_project_end(self, mock_periodic_filter):
        """Test project_end function"""
        # Create related objects
        models.Debugtalk.objects.create(project=self.project)
        models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body="{}"
        )
        models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        models.Report.objects.create(
            project=self.project,
            name="Test Report",
            type=1,
            status=1,
            creator="test"
        )
        models.Variables.objects.create(
            key="test_var",
            value="test_value",
            project=self.project
        )
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        models.CaseStep.objects.create(
            case=case,
            name="Step 1",
            url="/test",
            method="GET",
            body="{}",
            step=0
        )
        
        # Mock periodic task deletion
        mock_task_delete = Mock()
        mock_periodic_filter.return_value.delete = mock_task_delete
        
        # Call project_end
        prepare.project_end(self.project)
        
        # Verify all related objects are deleted
        self.assertFalse(models.Debugtalk.objects.filter(project=self.project).exists())
        self.assertFalse(models.Config.objects.filter(project=self.project).exists())
        self.assertFalse(models.API.objects.filter(project=self.project).exists())
        self.assertFalse(models.Report.objects.filter(project=self.project).exists())
        self.assertFalse(models.Variables.objects.filter(project=self.project).exists())
        self.assertFalse(models.CaseStep.objects.filter(case=case).exists())
        mock_task_delete.assert_called_once()

    def test_tree_end_type_1(self):
        """Test tree_end for type 1 (API)"""
        # Create API
        models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body="{}",
            relation=1
        )
        
        params = {"type": 1, "node": 1}
        prepare.tree_end(params, self.project)
        
        # Verify API is deleted
        self.assertFalse(models.API.objects.filter(relation=1, project=self.project).exists())

    def test_tree_end_type_2(self):
        """Test tree_end for type 2 (Case)"""
        # Create case and steps
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        models.CaseStep.objects.create(
            case=case,
            name="Step 1",
            url="/test",
            method="GET",
            body="{}",
            step=0
        )
        
        params = {"type": 2, "node": 1}
        prepare.tree_end(params, self.project)
        
        # Verify case and steps are deleted
        self.assertFalse(models.Case.objects.filter(id=case.id).exists())
        self.assertFalse(models.CaseStep.objects.filter(case=case).exists())

    @patch('fastrunner.utils.parser.Format')
    def test_update_casestep_with_format(self, mock_format):
        """Test update_casestep with Format parsing"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create existing step
        step = models.CaseStep.objects.create(
            case=case,
            name="Old Step",
            url="/old",
            method="GET",
            body="{}",
            step=0
        )
        
        # Mock Format
        mock_format_instance = Mock()
        mock_format_instance.name = "New Step"
        mock_format_instance.testcase = {"name": "New Step"}
        mock_format_instance.url = "/new"
        mock_format_instance.method = "POST"
        mock_format.return_value = mock_format_instance
        
        body = [{
            "id": step.id,
            "newBody": {"test": "data"},
            "case": case.id,
            "source_api_id": 123
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify step is updated
        updated_step = models.CaseStep.objects.get(id=step.id)
        self.assertEqual(updated_step.name, "New Step")
        self.assertEqual(updated_step.url, "/new")
        self.assertEqual(updated_step.method, "POST")

    def test_update_casestep_with_case_key(self):
        """Test update_casestep with case key"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create existing step
        step = models.CaseStep.objects.create(
            case=case,
            name="Old Step",
            url="/old",
            method="GET",
            body='{"name": "Old Step"}',
            step=0
        )
        
        body = [{
            "id": step.id,
            "case": case.id,
            "body": {"name": "New Step", "method": "GET", "url": "/new"},
            "source_api_id": 0
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify step is updated
        updated_step = models.CaseStep.objects.get(id=step.id)
        self.assertEqual(json.loads(updated_step.body)["name"], "New Step")

    def test_update_casestep_with_config(self):
        """Test update_casestep with config method"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create config
        config = models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body='{"name": "Test Config"}'
        )
        
        body = [{
            "id": config.id,
            "body": {"name": "Test Config", "method": "config"},
            "source_api_id": 0
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify new step is created
        new_step = models.CaseStep.objects.filter(case=case, method="config").first()
        self.assertIsNotNone(new_step)
        self.assertEqual(new_step.name, "Test Config")

    def test_update_casestep_with_api(self):
        """Test update_casestep with API"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create API
        api = models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body='{"name": "Test API"}',
            relation=1
        )
        
        body = [{
            "id": api.id,
            "body": {"name": "New API Name", "method": "POST", "url": "/new"},
            "source_api_id": 0
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify new step is created
        new_step = models.CaseStep.objects.filter(case=case).first()
        self.assertIsNotNone(new_step)
        self.assertEqual(json.loads(new_step.body)["name"], "New API Name")

    def test_update_casestep_is_copy(self):
        """Test update_casestep with is_copy flag"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        step = models.CaseStep.objects.create(
            case=case,
            name="Original Step",
            url="/test",
            method="GET",
            body='{"name": "Original Step"}',
            step=0
        )
        
        body = [{
            "id": step.id,
            "case": case.id,
            "is_copy": True,
            "body": {"name": "Copied Step", "method": "GET", "url": "/copy"},
            "source_api_id": 0
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify new step is created (not updated)
        self.assertEqual(models.CaseStep.objects.filter(case=case).count(), 2)

    def test_update_casestep_remove_extra_steps(self):
        """Test update_casestep removes extra steps"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=2
        )
        
        # Create two steps
        step1 = models.CaseStep.objects.create(
            case=case,
            name="Step 1",
            url="/test1",
            method="GET",
            body='{"name": "Step 1"}',
            step=0
        )
        step2 = models.CaseStep.objects.create(
            case=case,
            name="Step 2",
            url="/test2",
            method="GET",
            body='{"name": "Step 2"}',
            step=1
        )
        
        # Update only step1, step2 should be deleted
        body = [{
            "id": step1.id,
            "case": case.id,
            "body": {"name": "Updated Step", "method": "GET", "url": "/updated"},
            "source_api_id": 0
        }]
        
        prepare.update_casestep(body, case, "testuser")
        
        # Verify step2 is deleted
        self.assertFalse(models.CaseStep.objects.filter(id=step2.id).exists())
        self.assertTrue(models.CaseStep.objects.filter(id=step1.id).exists())

    @patch('fastrunner.utils.parser.Format')
    def test_generate_casestep_with_format(self, mock_format):
        """Test generate_casestep with Format parsing"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Mock Format
        mock_format_instance = Mock()
        mock_format_instance.name = "New Step"
        mock_format_instance.testcase = {"name": "New Step"}
        mock_format_instance.url = "/new"
        mock_format_instance.method = "POST"
        mock_format.return_value = mock_format_instance
        
        body = [{
            "newBody": {"test": "data"}
        }]
        
        prepare.generate_casestep(body, case, "testuser")
        
        # Verify step is created
        step = models.CaseStep.objects.filter(case=case).first()
        self.assertIsNotNone(step)
        self.assertEqual(step.name, "New Step")
        self.assertEqual(step.url, "/new")
        self.assertEqual(step.method, "POST")

    def test_generate_casestep_with_config(self):
        """Test generate_casestep with config"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create config
        config = models.Config.objects.create(
            name="Test Config",
            project=self.project,
            body='{"name": "Test Config"}',
            base_url="http://test.com"
        )
        
        body = [{
            "body": {"name": "Test Config", "method": "config"}
        }]
        
        prepare.generate_casestep(body, case, "testuser")
        
        # Verify step is created
        step = models.CaseStep.objects.filter(case=case).first()
        self.assertIsNotNone(step)
        self.assertEqual(step.name, "Test Config")
        self.assertEqual(step.method, "config")
        self.assertEqual(step.url, "http://test.com")

    def test_generate_casestep_with_api(self):
        """Test generate_casestep with API"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        # Create API
        api = models.API.objects.create(
            name="Test API",
            project=self.project,
            method="GET",
            url="/test",
            body='{"name": "Test API"}',
            relation=1
        )
        
        body = [{
            "id": api.id,
            "body": {"name": "New Name", "url": "/new", "method": "POST"}
        }]
        
        prepare.generate_casestep(body, case, "testuser")
        
        # Verify step is created
        step = models.CaseStep.objects.filter(case=case).first()
        self.assertIsNotNone(step)
        self.assertEqual(json.loads(step.body)["name"], "New Name")
        self.assertEqual(step.url, "/new")
        self.assertEqual(step.method, "POST")

    def test_case_end_single_id(self):
        """Test case_end with single id"""
        case = models.Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        prepare.case_end(case.id)
        
        # Verify case is deleted
        self.assertFalse(models.Case.objects.filter(id=case.id).exists())

    def test_case_end_list_ids(self):
        """Test case_end with list of ids"""
        case1 = models.Case.objects.create(
            name="Test Case 1",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        case2 = models.Case.objects.create(
            name="Test Case 2",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        prepare.case_end([case1.id, case2.id])
        
        # Verify both cases are deleted
        self.assertFalse(models.Case.objects.filter(id__in=[case1.id, case2.id]).exists())

    def test_case_end_invalid_type(self):
        """Test case_end with invalid type"""
        # Should return without error
        prepare.case_end("invalid")
        prepare.case_end(None)