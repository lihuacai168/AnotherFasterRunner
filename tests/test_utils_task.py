import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from fastrunner.utils import response
from fastrunner.utils.task import Task


class TestTask:
    """Test cases for Task class"""

    def get_valid_task_data(self):
        """Helper method to get valid task data"""
        return {
            "name": "Test Task",
            "data": {"test": "data"},
            "crontab": "0 0 * * *",
            "switch": True,
            "project": "Test Project",
            "strategy": "始终发送",
            "webhook": "http://example.com/webhook",
            "mail_cc": "cc@example.com",
            "receiver": "receiver@example.com",
            "updater": "test_updater",
            "creator": "test_creator",
            "ci_project_ids": [1, 2, 3],
            "ci_env": "test",
            "is_parallel": True,
            "config": "test_config"
        }

    def test_task_init(self):
        """Test Task initialization"""
        task_data = self.get_valid_task_data()
        
        with patch('fastrunner.utils.task.logger') as mock_logger:
            task = Task(**task_data)
            
            # Verify logger was called
            mock_logger.info.assert_called_once()
            
            # Verify private attributes are set correctly
            assert task._Task__name == "Test Task"
            assert task._Task__data == {"test": "data"}
            assert task._Task__crontab == "0 0 * * *"
            assert task._Task__switch is True
            assert task._Task__task == "fastrunner.tasks.schedule_debug_suite"
            assert task._Task__project == "Test Project"
            
            # Verify email dict is constructed correctly
            expected_email = {
                "strategy": "始终发送",
                "mail_cc": "cc@example.com",
                "receiver": "receiver@example.com",
                "crontab": "0 0 * * *",
                "project": "Test Project",
                "task_name": "Test Task",
                "webhook": "http://example.com/webhook",
                "updater": "test_updater",
                "creator": "test_creator",
                "ci_project_ids": [1, 2, 3],
                "ci_env": "test",
                "is_parallel": True,
                "config": "test_config"
            }
            assert task._Task__email == expected_email
            assert task._Task__crontab_time is None

    def test_task_init_with_minimal_data(self):
        """Test Task initialization with minimal required data"""
        minimal_data = {
            "name": "Minimal Task",
            "data": {},
            "crontab": "* * * * *",
            "switch": False,
            "project": "Project",
            "strategy": "仅失败发送",
            "webhook": ""
        }
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**minimal_data)
            
            # Verify defaults are used for optional fields
            assert task._Task__email["mail_cc"] is None
            assert task._Task__email["receiver"] is None
            assert task._Task__email["updater"] is None
            assert task._Task__email["creator"] is None
            assert task._Task__email["ci_project_ids"] == []
            assert task._Task__email["ci_env"] == "请选择"
            assert task._Task__email["is_parallel"] is False
            assert task._Task__email["config"] == "请选择"

    def test_format_crontab_success(self):
        """Test successful crontab formatting"""
        task_data = self.get_valid_task_data()
        task_data["crontab"] = "30 2 15 4 1"  # Valid 5-part crontab
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.format_crontab()
            
            assert result == response.TASK_ADD_SUCCESS
            assert task._Task__crontab_time == {
                "minute": "30",
                "hour": "2",
                "day_of_month": "15",
                "month_of_year": "4",
                "day_of_week": "1"
            }

    def test_format_crontab_too_many_fields(self):
        """Test crontab with too many fields"""
        task_data = self.get_valid_task_data()
        task_data["crontab"] = "30 2 15 4 1 extra"  # 6 fields instead of 5
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.format_crontab()
            
            assert result == response.TASK_TIME_ILLEGAL

    def test_format_crontab_too_few_fields(self):
        """Test crontab with too few fields"""
        task_data = self.get_valid_task_data()
        task_data["crontab"] = "30 2"  # Only 2 fields instead of 5
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.format_crontab()
            
            assert result == response.TASK_TIME_ILLEGAL

    def test_format_crontab_exception(self):
        """Test crontab formatting with exception"""
        task_data = self.get_valid_task_data()
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            # Simulate split returning unexpected result
            with patch.object(task._Task__crontab, 'split', return_value=[]):
                result = task.format_crontab()
                assert result == response.TASK_TIME_ILLEGAL

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_already_exists(self, mock_celery_models):
        """Test adding task that already exists"""
        task_data = self.get_valid_task_data()
        
        # Mock task already exists
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 1
        
        with patch('fastrunner.utils.task.logger') as mock_logger:
            task = Task(**task_data)
            result = task.add_task()
            
            assert result == response.TASK_HAS_EXISTS
            # Verify logger message
            mock_logger.info.assert_any_call("Test Task tasks exist")

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_invalid_crontab(self, mock_celery_models):
        """Test adding task with invalid crontab"""
        task_data = self.get_valid_task_data()
        task_data["crontab"] = "invalid crontab"
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.add_task()
            
            assert result == response.TASK_TIME_ILLEGAL

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_success_new_crontab(self, mock_celery_models):
        """Test successfully adding task with new crontab schedule"""
        task_data = self.get_valid_task_data()
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        # Mock crontab doesn't exist
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = None
        
        # Mock created objects
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.create.return_value = mock_crontab
        
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger') as mock_logger:
            task = Task(**task_data)
            result = task.add_task()
            
            assert result == response.TASK_ADD_SUCCESS
            
            # Verify crontab creation
            expected_crontab_time = {
                "minute": "0",
                "hour": "0",
                "day_of_month": "*",
                "month_of_year": "*",
                "day_of_week": "*"
            }
            mock_celery_models.CrontabSchedule.objects.create.assert_called_once_with(**expected_crontab_time)
            
            # Verify task creation
            mock_celery_models.PeriodicTask.objects.get_or_create.assert_called_once_with(
                name="Test Task",
                task="fastrunner.tasks.schedule_debug_suite",
                crontab=mock_crontab
            )
            
            # Verify task attributes are set
            assert mock_task.crontab == mock_crontab
            assert mock_task.enabled is True
            mock_task.save.assert_called_once()
            
            # Verify logger message
            mock_logger.info.assert_any_call("Test Task tasks save success")

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_success_existing_crontab(self, mock_celery_models):
        """Test successfully adding task with existing crontab schedule"""
        task_data = self.get_valid_task_data()
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        # Mock crontab exists
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        # Mock task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.add_task()
            
            assert result == response.TASK_ADD_SUCCESS
            
            # Verify crontab was not created (using existing)
            mock_celery_models.CrontabSchedule.objects.create.assert_not_called()
            
            # Verify task uses existing crontab
            assert mock_task.crontab == mock_crontab

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_with_email_strategy_always_send_no_receiver(self, mock_celery_models):
        """Test adding task with email strategy '始终发送' but no receiver"""
        task_data = self.get_valid_task_data()
        task_data["strategy"] = "始终发送"
        task_data["receiver"] = ""
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        # Mock crontab
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        # Mock task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.add_task()
            
            # Should still succeed (commented out return in original code)
            assert result == response.TASK_ADD_SUCCESS

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_with_email_strategy_fail_only_no_receiver(self, mock_celery_models):
        """Test adding task with email strategy '仅失败发送' but no receiver"""
        task_data = self.get_valid_task_data()
        task_data["strategy"] = "仅失败发送"
        task_data["receiver"] = ""
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        # Mock crontab
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        # Mock task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.add_task()
            
            # Should still succeed (commented out return in original code)
            assert result == response.TASK_ADD_SUCCESS

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_verify_json_encoding(self, mock_celery_models):
        """Test that task data and email are properly JSON encoded"""
        task_data = self.get_valid_task_data()
        task_data["data"] = {"中文": "测试", "unicode": "test"}
        
        # Mock setup
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.add_task()
            
            # Verify JSON encoding with ensure_ascii=False
            expected_args = json.dumps({"中文": "测试", "unicode": "test"}, ensure_ascii=False)
            assert mock_task.args == expected_args
            
            # Verify kwargs (email) encoding
            kwargs_dict = json.loads(mock_task.kwargs)
            assert kwargs_dict["task_name"] == "Test Task"

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_success_new_crontab(self, mock_celery_models):
        """Test successfully updating task with new crontab"""
        task_data = self.get_valid_task_data()
        task_id = 123
        
        # Mock existing task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get.return_value = mock_task
        
        # Mock crontab doesn't exist
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = None
        
        # Mock new crontab
        mock_new_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.create.return_value = mock_new_crontab
        
        with patch('fastrunner.utils.task.logger') as mock_logger:
            task = Task(**task_data)
            result = task.update_task(task_id)
            
            assert result == response.TASK_UPDATE_SUCCESS
            
            # Verify task lookup
            mock_celery_models.PeriodicTask.objects.get.assert_called_once_with(id=task_id)
            
            # Verify crontab creation
            expected_crontab_time = {
                "minute": "0",
                "hour": "0",
                "day_of_month": "*",
                "month_of_year": "*",
                "day_of_week": "*"
            }
            mock_celery_models.CrontabSchedule.objects.create.assert_called_once_with(**expected_crontab_time)
            
            # Verify task update
            assert mock_task.crontab == mock_new_crontab
            assert mock_task.enabled is True
            assert mock_task.name == "Test Task"
            assert mock_task.description == "Test Project"
            mock_task.save.assert_called_once()
            
            # Verify logger message
            mock_logger.info.assert_any_call("Test Task tasks save success")

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_success_existing_crontab(self, mock_celery_models):
        """Test successfully updating task with existing crontab"""
        task_data = self.get_valid_task_data()
        task_id = 456
        
        # Mock existing task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get.return_value = mock_task
        
        # Mock crontab exists
        mock_existing_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_existing_crontab
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.update_task(task_id)
            
            assert result == response.TASK_UPDATE_SUCCESS
            
            # Verify crontab was not created
            mock_celery_models.CrontabSchedule.objects.create.assert_not_called()
            
            # Verify task uses existing crontab
            assert mock_task.crontab == mock_existing_crontab

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_invalid_crontab(self, mock_celery_models):
        """Test updating task with invalid crontab"""
        task_data = self.get_valid_task_data()
        task_data["crontab"] = "invalid"
        task_id = 789
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.update_task(task_id)
            
            assert result == response.TASK_TIME_ILLEGAL
            
            # Verify task was not retrieved
            mock_celery_models.PeriodicTask.objects.get.assert_not_called()

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_with_changed_name(self, mock_celery_models):
        """Test updating task with changed name"""
        task_data = self.get_valid_task_data()
        task_data["name"] = "Updated Task Name"
        task_id = 999
        
        # Mock existing task
        mock_task = MagicMock()
        mock_task.name = "Old Task Name"
        mock_celery_models.PeriodicTask.objects.get.return_value = mock_task
        
        # Mock crontab
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.update_task(task_id)
            
            assert result == response.TASK_UPDATE_SUCCESS
            assert mock_task.name == "Updated Task Name"

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_all_fields(self, mock_celery_models):
        """Test updating all task fields"""
        task_data = self.get_valid_task_data()
        task_data["switch"] = False  # Change enabled state
        task_data["data"] = {"new": "data"}
        task_data["project"] = "Updated Project"
        task_id = 111
        
        # Mock existing task
        mock_task = MagicMock()
        mock_celery_models.PeriodicTask.objects.get.return_value = mock_task
        
        # Mock crontab
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            result = task.update_task(task_id)
            
            assert result == response.TASK_UPDATE_SUCCESS
            
            # Verify all fields updated
            assert mock_task.enabled is False
            assert mock_task.args == json.dumps({"new": "data"}, ensure_ascii=False)
            assert mock_task.description == "Updated Project"
            
            # Verify kwargs updated
            kwargs_dict = json.loads(mock_task.kwargs)
            assert kwargs_dict["project"] == "Updated Project"

    def test_task_with_special_characters_in_data(self):
        """Test task with special characters in data"""
        task_data = self.get_valid_task_data()
        task_data["data"] = {
            "special": "Hello\nWorld\t测试",
            "quotes": 'He said "Hello"',
            "emoji": "😀🎉"
        }
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            
            # Verify data is stored correctly
            assert task._Task__data["special"] == "Hello\nWorld\t测试"
            assert task._Task__data["quotes"] == 'He said "Hello"'
            assert task._Task__data["emoji"] == "😀🎉"

    @patch('fastrunner.utils.task.celery_models')
    def test_add_task_database_error(self, mock_celery_models):
        """Test add_task handling database errors gracefully"""
        task_data = self.get_valid_task_data()
        
        # Mock task doesn't exist
        mock_celery_models.PeriodicTask.objects.filter.return_value.count.return_value = 0
        
        # Mock database error during save
        mock_crontab = MagicMock()
        mock_celery_models.CrontabSchedule.objects.filter.return_value.first.return_value = mock_crontab
        
        mock_task = MagicMock()
        mock_task.save.side_effect = Exception("Database error")
        mock_celery_models.PeriodicTask.objects.get_or_create.return_value = (mock_task, True)
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            
            # This should raise the exception
            with pytest.raises(Exception, match="Database error"):
                task.add_task()

    @patch('fastrunner.utils.task.celery_models')
    def test_update_task_not_found(self, mock_celery_models):
        """Test update_task when task doesn't exist"""
        task_data = self.get_valid_task_data()
        task_id = 404
        
        # Mock task not found
        mock_celery_models.PeriodicTask.objects.get.side_effect = mock_celery_models.PeriodicTask.DoesNotExist
        
        with patch('fastrunner.utils.task.logger'):
            task = Task(**task_data)
            
            # This should raise the exception
            with pytest.raises(AttributeError):
                task.update_task(task_id)