"""Test for fastrunner.tasks module"""
import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase
from django_celery_beat.models import PeriodicTask

from fastrunner.models import API, Case, CaseStep, Config, Project
from fastrunner.tasks import (
    MyBaseTask,
    async_debug_api,
    async_debug_suite,
    schedule_debug_suite,
    update_task_total_run_count,
)


@pytest.mark.django_db
class TestTasks(TestCase):
    """Test task functions"""

    def setUp(self):
        self.project = Project.objects.create(
            name="Task Test Project",
            desc="Project for task testing",
            responsible="taskuser"
        )
        
        self.config = Config.objects.create(
            name="Task Config",
            project=self.project,
            body=json.dumps({
                "name": "Task Config",
                "request": {
                    "base_url": "http://localhost:8000"
                }
            })
        )
        
        self.api = API.objects.create(
            name="Task API",
            project=self.project,
            method="GET",
            url="/api/test",
            body=json.dumps({
                "name": "Task API",
                "request": {
                    "url": "/api/test",
                    "method": "GET"
                }
            }),
            relation=1
        )
        
        self.case = Case.objects.create(
            name="Task Case",
            project=self.project,
            tag=1,
            relation=1,
            length=1
        )
        
        self.case_step = CaseStep.objects.create(
            case=self.case,
            name="Step 1",
            step=1,
            source_api_id=self.api.id,
            body=json.dumps({
                "name": "Step 1",
                "request": {
                    "url": "/api/test",
                    "method": "GET"
                }
            }),
            url=self.api.url,
            method=self.api.method
        )

    @patch('django_celery_beat.models.PeriodicTask.objects.get')
    @patch('django_celery_beat.models.PeriodicTask.objects.filter')
    def test_update_task_total_run_count(self, mock_filter, mock_get):
        """Test update_task_total_run_count function"""
        mock_task = MagicMock()
        mock_task.total_run_count = 5
        mock_task.date_changed = "2023-01-01"
        mock_get.return_value = mock_task
        mock_filter.return_value.update = MagicMock()
        
        update_task_total_run_count(1)
        
        mock_get.assert_called_once_with(id=1)
        mock_filter.assert_called_once_with(id=1)
        mock_filter.return_value.update.assert_called_once_with(
            date_changed="2023-01-01", 
            total_run_count=6
        )
        
    def test_update_task_total_run_count_none(self):
        """Test update_task_total_run_count with None task_id"""
        # Should not raise exception
        update_task_total_run_count(None)

    def test_my_base_task(self):
        """Test MyBaseTask class"""
        task = MyBaseTask()
        
        # Test run method
        result = task.run()
        self.assertIsNone(result)
        
        # Test on_failure
        with patch('fastrunner.tasks.update_task_total_run_count') as mock_update:
            task.on_failure(
                exc=Exception("Test error"),
                task_id="test-task-id",
                args=[],
                kwargs={"task_id": 123},
                einfo=None
            )
            mock_update.assert_called_once_with(123)
        
        # Test on_success
        with patch('fastrunner.tasks.update_task_total_run_count') as mock_update:
            task.on_success(
                retval="success",
                task_id="test-task-id",
                args=[],
                kwargs={"task_id": 456}
            )
            mock_update.assert_called_once_with(456)

    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_api')
    def test_async_debug_api(self, mock_debug_api, mock_save_summary):
        """Test async_debug_api task"""
        mock_debug_api.return_value = {"success": True}
        mock_save_summary.return_value = 1
        
        async_debug_api(
            api=self.api.id,
            project=self.project.id,
            name="Test API Run",
            config=self.config.id
        )
        
        mock_debug_api.assert_called_once_with(
            self.api.id,
            self.project.id,
            config=self.config.id,
            save=False
        )
        mock_save_summary.assert_called_once_with(
            "Test API Run",
            {"success": True},
            self.project.id
        )

    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_suite')
    def test_async_debug_suite(self, mock_debug_suite, mock_save_summary):
        """Test async_debug_suite task"""
        mock_debug_suite.return_value = ({"success": True}, None)
        mock_save_summary.return_value = 1
        
        async_debug_suite(
            suite=[self.case.id],
            project=self.project.id,
            obj="test",
            report="Test Suite Run",
            config=self.config.id,
            user="testuser"
        )
        
        mock_debug_suite.assert_called_once_with(
            [self.case.id],
            self.project.id,
            "test",
            config=self.config.id,
            save=False
        )
        mock_save_summary.assert_called_once_with(
            name="Test Suite Run",
            summary={"success": True},
            project=self.project.id,
            type=2,
            user="testuser"
        )

    @patch('fastrunner.tasks.lark_message.send_message')
    @patch('fastrunner.tasks.DingMessage')
    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_suite')
    def test_schedule_debug_suite_with_ding(self, mock_debug_suite, mock_save_summary, 
                                            mock_ding_class, mock_lark_send):
        """Test schedule_debug_suite with DingTalk webhook"""
        # Setup mocks
        mock_debug_suite.return_value = ({
            "success": True,
            "stat": {"failures": 1, "successes": 9}
        }, None)
        mock_save_summary.return_value = 1001
        mock_ding_instance = MagicMock()
        mock_ding_class.return_value = mock_ding_instance
        
        # Create config step
        config_step = CaseStep.objects.create(
            case=self.case,
            name="Config Step",
            step=0,
            body=json.dumps({
                "name": "Task Config",
                "request": {
                    "base_url": "http://localhost:8000"
                }
            }),
            url="",
            method="CONFIG"
        )
        
        schedule_debug_suite(
            self.case.id,
            project=self.project.id,
            task_name="Scheduled Test",
            strategy="仅失败发送",
            webhook="https://oapi.dingtalk.com/robot/send",
            user="scheduler",
            is_parallel=True,
            config="Task Config",
            task_id=123
        )
        
        # Verify calls
        mock_save_summary.assert_called_once()
        self.assertEqual(mock_save_summary.call_args[0][0], "Scheduled Test")
        self.assertEqual(mock_save_summary.call_args[1]["type"], 3)
        
        # Verify DingTalk message sent
        mock_ding_class.assert_called_once_with(webhook="https://oapi.dingtalk.com/robot/send")
        mock_ding_instance.send_ding_msg.assert_called_once()

    @patch('fastrunner.tasks.lark_message.send_message')
    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_suite')
    def test_schedule_debug_suite_with_feishu(self, mock_debug_suite, mock_save_summary, 
                                              mock_lark_send):
        """Test schedule_debug_suite with Feishu webhook"""
        mock_debug_suite.return_value = ({
            "success": True,
            "stat": {"failures": 0, "successes": 10}
        }, None)
        mock_save_summary.return_value = 2001
        
        schedule_debug_suite(
            self.case.id,
            project=self.project.id,
            task_name="Deploy Test",
            strategy="始终发送",
            webhook="https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
            run_type="deploy",
            task_id=456
        )
        
        # Verify save_summary called with deploy type
        mock_save_summary.assert_called_once()
        self.assertEqual(mock_save_summary.call_args[0][0], "部署_Deploy Test")
        self.assertEqual(mock_save_summary.call_args[1]["type"], 4)
        
        # Verify Feishu message sent
        mock_lark_send.assert_called_once()
        call_args = mock_lark_send.call_args
        self.assertEqual(call_args[1]["webhook"], "https://open.feishu.cn/open-apis/bot/v2/hook/xxx")
        self.assertEqual(call_args[1]["summary"]["task_name"], "部署_Deploy Test")
        self.assertEqual(call_args[1]["summary"]["report_id"], 2001)

    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_suite')
    def test_schedule_debug_suite_no_webhook(self, mock_debug_suite, mock_save_summary):
        """Test schedule_debug_suite without webhook"""
        mock_debug_suite.return_value = ({
            "success": True,
            "stat": {"failures": 0, "successes": 10}
        }, None)
        mock_save_summary.return_value = 3001
        
        schedule_debug_suite(
            self.case.id,
            project=self.project.id,
            task_name="No Webhook Test",
            strategy="仅失败发送",
            task_id=789
        )
        
        # Verify save_summary called
        mock_save_summary.assert_called_once()
        self.assertEqual(mock_save_summary.call_args[0][0], "No Webhook Test")

    @patch('fastrunner.tasks.save_summary')
    @patch('fastrunner.tasks.debug_suite')
    def test_schedule_debug_suite_invalid_webhook(self, mock_debug_suite, mock_save_summary):
        """Test schedule_debug_suite with invalid webhook"""
        mock_debug_suite.return_value = ({
            "success": True,
            "stat": {"failures": 1, "successes": 9}
        }, None)
        mock_save_summary.return_value = 4001
        
        # Test with unsupported webhook
        schedule_debug_suite(
            self.case.id,
            project=self.project.id,
            task_name="Invalid Webhook Test",
            strategy="始终发送",
            webhook="https://invalid.webhook.com/hook",
            task_id=999
        )
        
        # Verify save_summary still called
        mock_save_summary.assert_called_once()

    @patch('fastrunner.models.Case.objects.get')
    def test_schedule_debug_suite_missing_case(self, mock_case_get):
        """Test schedule_debug_suite with non-existent case"""
        from django.core.exceptions import ObjectDoesNotExist
        
        mock_case_get.side_effect = ObjectDoesNotExist()
        
        with patch('fastrunner.tasks.debug_suite') as mock_debug_suite:
            with patch('fastrunner.tasks.save_summary') as mock_save_summary:
                mock_debug_suite.return_value = ({"success": True, "stat": {"failures": 0}}, None)
                mock_save_summary.return_value = 5001
                
                # Should not raise exception
                schedule_debug_suite(
                    99999,  # Non-existent case ID
                    project=self.project.id,
                    task_name="Missing Case Test",
                    strategy="仅失败发送",
                    task_id=1111
                )
                
                # debug_suite should be called with empty suite
                mock_debug_suite.assert_called_once()
                self.assertEqual(mock_debug_suite.call_args[0][0], [])  # Empty test_sets