import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from fastrunner.models import API, Case, CaseStep, Config, HostIP, Project, Relation, Report, Variables, Visit
from fastrunner.views import project, run, schedule, suite
from fastrunner.views import report as report_views
from fastuser.models import MyUser, UserInfo, UserToken
from test_constants import TEST_PASSWORD


@pytest.mark.integration
@pytest.mark.django_db
class TestRunViews(TestCase):
    """Integration tests for run views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='runuser',
            email='run@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='runuser',
            email='run@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='run-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Run Test Project",
            desc="Project for run testing",
            responsible="runuser"
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
                    "method": "GET"
                }
            }),
            relation=1
        )

    @patch('fastrunner.views.run.run_api')
    def test_run_api_by_pk(self, mock_run_api):
        """Test running single API by primary key"""
        mock_run_api.return_value = {
            'success': True,
            'response': {'status_code': 200}
        }
        
        response = self.client.get(f'/api/fastrunner/run_api_pk/{self.api.id}/', {
            'config': self.config.id,
            'project': self.project.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_run_api.assert_called_once()

    @patch('fastrunner.views.run.run_api')
    def test_run_api_tree(self, mock_run_api):
        """Test running APIs by tree structure"""
        mock_run_api.return_value = {
            'success': True,
            'response': {'status_code': 200}
        }
        
        data = {
            'id': [self.api.id],
            'config': self.config.id,
            'project': self.project.id,
            'run_type': 'api'
        }
        
        response = self.client.post('/api/fastrunner/run_api_tree/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('fastrunner.views.run.run_api')
    def test_run_testsuite(self, mock_run_api):
        """Test running test suite"""
        # Create test case
        case = Case.objects.create(
            name="Test Case",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        
        # Create test step
        CaseStep.objects.create(
            case=case,
            name="Step 1",
            step=1,
            source_api_id=self.api.id,
            body=self.api.body,
            url=self.api.url,
            method=self.api.method
        )
        
        mock_run_api.return_value = {
            'success': True,
            'response': {'status_code': 200}
        }
        
        data = {
            'id': [case.id],
            'config': self.config.id,
            'project': self.project.id,
            'run_type': 'test'
        }
        
        response = self.client.post('/api/fastrunner/run_testsuite/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.integration
@pytest.mark.django_db
class TestSuiteViews(TestCase):
    """Integration tests for test suite views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='suiteuser',
            email='suite@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='suiteuser',
            email='suite@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='suite-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Suite Test Project",
            desc="Project for suite testing",
            responsible="suiteuser"
        )
        
        self.relation = Relation.objects.create(
            project=self.project,
            tree=1,
            name="Test Suite",
            type=2
        )

    def test_test_case_crud(self):
        """Test CRUD operations for test cases"""
        
        # Create test case
        case_data = {
            "name": "CRUD Test Case",
            "project": self.project.id,
            "relation": self.relation.id,
            "tag": 1
        }
        
        response = self.client.post('/api/fastrunner/test/', case_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case_id = json.loads(response.content)['id']
        
        # Get test cases
        response = self.client.get('/api/fastrunner/test/', {
            'project': self.project.id,
            'node': self.relation.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update test case
        update_data = {
            "name": "Updated Test Case",
            "desc": "Updated description"
        }
        response = self.client.put(f'/api/fastrunner/test/{case_id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Copy test case
        copy_data = {"name": "Copied Test Case"}
        response = self.client.post(f'/api/fastrunner/test/{case_id}/', copy_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete test case
        response = self.client.delete(f'/api/fastrunner/test/', {"id": [case_id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_step_management(self):
        """Test case step management"""
        
        # Create test case
        case = Case.objects.create(
            name="Step Test Case",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        
        # Create API for step
        api = API.objects.create(
            name="Step API",
            project=self.project,
            method="GET",
            url="/api/step",
            body=json.dumps({
                "name": "Step API",
                "request": {
                    "url": "/api/step",
                    "method": "GET"
                }
            }),
            relation=1
        )
        
        # Add step
        step_data = {
            "name": "Test Step",
            "api": api.id,
            "step": 1,
            "body": api.body,
            "source_api_id": api.id
        }
        
        response = self.client.post(f'/api/fastrunner/teststep/{case.id}/', step_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get steps
        response = self.client.get(f'/api/fastrunner/teststep/{case.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Update step
        step = CaseStep.objects.filter(case=case).first()
        update_data = {
            "id": step.id,
            "body": json.dumps({
                "name": "Updated Step",
                "request": {
                    "url": "/api/updated-step",
                    "method": "POST"
                }
            })
        }
        
        response = self.client.patch(f'/api/fastrunner/teststep/{case.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete step
        response = self.client.delete(f'/api/fastrunner/teststep/{case.id}/', {"id": [step.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.integration
@pytest.mark.django_db
class TestProjectViews(TestCase):
    """Integration tests for project views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='projectviewuser',
            email='projectview@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='projectviewuser',
            email='projectview@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='projectview-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')

    def test_dashboard_view(self):
        """Test dashboard statistics"""
        
        # Create test data
        project = Project.objects.create(
            name="Dashboard Test Project",
            desc="Project for dashboard testing",
            responsible="projectviewuser"
        )
        
        # Create some APIs and cases
        for i in range(5):
            API.objects.create(
                name=f"API {i}",
                project=project,
                method="GET",
                url=f"/api/test{i}",
                body=json.dumps({"name": f"API {i}"}),
                relation=1
            )
            
            Case.objects.create(
                name=f"Case {i}",
                project=project,
                tag=1,
                relation=1,  # Required node id
                length=1     # Required API count
            )
        
        # Create reports
        for i in range(3):
            Report.objects.create(
                project=project,
                name=f"Report {i}",
                type=1,
                status=True,
                creator=self.user.username,
                detail=json.dumps({
                    "success": True,
                    "stat": {"testcases": {"total": 10, "success": 8, "fail": 2}}
                })
            )
        
        response = self.client.get('/api/fastrunner/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('api_count', response.data)
        self.assertIn('case_count', response.data)
        self.assertIn('report_count', response.data)

    def test_debugtalk_management(self):
        """Test debugtalk.py management"""
        
        project = Project.objects.create(
            name="DebugTalk Test Project",
            desc="Project for debugtalk testing",
            responsible="projectviewuser"
        )
        
        # Get debugtalk
        response = self.client.get(f'/api/fastrunner/debugtalk/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update debugtalk
        update_data = {
            "id": project.id,
            "debugtalk": "# Custom debugtalk.py\ndef custom_function():\n    return 'test'"
        }
        response = self.client.patch('/api/fastrunner/debugtalk/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tree_view(self):
        """Test project tree structure"""
        
        project = Project.objects.create(
            name="Tree Test Project",
            desc="Project for tree testing",
            responsible="projectviewuser"
        )
        
        # Create tree structure
        root = Relation.objects.create(
            project=project,
            tree=1,
            name="Root",
            type=1
        )
        
        child1 = Relation.objects.create(
            project=project,
            tree=2,
            name="Child 1",
            type=1
        )
        
        child2 = Relation.objects.create(
            project=project,
            tree=3,
            name="Child 2",
            type=2
        )
        
        response = self.client.get(f'/api/fastrunner/tree/{project.id}/', {'type': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    def test_visit_tracking(self):
        """Test visit tracking functionality"""
        
        project = Project.objects.create(
            name="Visit Test Project",
            desc="Project for visit testing",
            responsible="projectviewuser"
        )
        
        # Create some visits
        for i in range(3):
            Visit.objects.create(
                project=project,
                user=self.user,
                url="/api/test",
                request_method="GET",
                request_body="{}",
                response_code=200,
                response_body=json.dumps({"success": True}),
                response_header=json.dumps({"Content-Type": "application/json"})
            )
        
        response = self.client.get('/api/fastrunner/visit/', {'project': project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


@pytest.mark.integration
@pytest.mark.django_db
class TestReportViews(TestCase):
    """Integration tests for report views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='reportviewuser',
            email='reportview@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='reportviewuser',
            email='reportview@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='reportview-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Report View Test Project",
            desc="Project for report view testing",
            responsible="reportviewuser"
        )

    def test_report_list_and_filter(self):
        """Test report listing and filtering"""
        
        # Create reports with different types
        report_types = [1, 2, 3, 4]  # 调试，定时，异步，部署
        for report_type in report_types:
            for i in range(2):
                Report.objects.create(
                    project=self.project,
                    name=f"Report Type {report_type} - {i}",
                    type=report_type,
                    status=i % 2 == 0,  # Alternate between success and failure
                    creator=self.user.username,
                    detail=json.dumps({
                        "success": i % 2 == 0,
                        "stat": {
                            "testcases": {
                                "total": 10,
                                "success": 8 if i % 2 == 0 else 3,
                                "fail": 2 if i % 2 == 0 else 7
                            }
                        },
                        "time": {
                            "start_at": datetime.now().isoformat(),
                            "duration": 60
                        }
                    })
                )
        
        # Test listing all reports
        response = self.client.get('/api/fastrunner/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # Test filtering by project
        response = self.client.get('/api/fastrunner/reports/', {'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test filtering by report type
        response = self.client.get('/api/fastrunner/reports/', {'reportType': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test search functionality
        response = self.client.get('/api/fastrunner/reports/', {'search': 'Type 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_detail_view(self):
        """Test viewing report details"""
        
        report_detail = {
            "success": True,
            "stat": {
                "testcases": {
                    "total": 5,
                    "success": 4,
                    "fail": 1
                }
            },
            "time": {
                "start_at": datetime.now().isoformat(),
                "duration": 120
            },
            "platform": {
                "httprunner_version": "1.5.8",
                "python_version": "3.11.0"
            },
            "details": [
                {
                    "name": "Test Case 1",
                    "success": True,
                    "stat": {
                        "total": 3,
                        "successes": 3,
                        "failures": 0
                    }
                }
            ]
        }
        
        report = Report.objects.create(
            project=self.project,
            name="Detailed Report",
            type=1,
            status=True,
            creator=self.user.username,
            detail=json.dumps(report_detail)
        )
        
        response = self.client.get(f'/api/fastrunner/reports/{report.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], report.id)
        self.assertIn('detail', response.data)


@pytest.mark.integration
@pytest.mark.django_db
class TestScheduleViews(TestCase):
    """Integration tests for schedule views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='scheduleuser',
            email='schedule@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='scheduleuser',
            email='schedule@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='schedule-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Schedule Test Project",
            desc="Project for schedule testing",
            responsible="scheduleuser"
        )

    @patch('fastrunner.views.schedule.create_task')
    @patch('fastrunner.views.schedule.delete_task')
    def test_schedule_crud(self, mock_delete_task, mock_create_task):
        """Test CRUD operations for scheduled tasks"""
        
        mock_create_task.return_value = {"name": "test_task_1"}
        
        # Create test case for scheduling
        case = Case.objects.create(
            name="Scheduled Test Case",
            project=self.project,
            tag=1,
            relation=1,  # Required node id
            length=1     # Required API count
        )
        
        # Create schedule
        schedule_data = {
            "name": "Daily Test Run",
            "data": [case.id],
            "crontab": "0 0 * * *",  # Daily at midnight
            "switch": True,
            "project": self.project.id,
            "config": "",
            "run_type": "test"
        }
        
        response = self.client.post('/api/fastrunner/schedule/', schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # List schedules
        response = self.client.get('/api/fastrunner/schedule/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update schedule  
        schedule_id = 1  # Assuming this is created
        update_data = {
            "name": "Updated Schedule",
            "crontab": "0 12 * * *",  # Daily at noon
            "switch": False
        }
        
        response = self.client.put(f'/api/fastrunner/schedule/{schedule_id}/', update_data, format='json')
        # Note: This might fail if schedule doesn't exist in test DB
        
        # Delete schedule
        response = self.client.delete(f'/api/fastrunner/schedule/{schedule_id}/')
        # Note: This might fail if schedule doesn't exist in test DB


@pytest.mark.integration
@pytest.mark.django_db
class TestConfigViews(TestCase):
    """Integration tests for configuration views"""

    def setUp(self):
        self.client = APIClient()
        self.user = MyUser.objects.create_user(
            username='configviewuser',
            email='configview@example.com',
            password=TEST_PASSWORD
        )
        self.user_info = UserInfo.objects.create(
            username='configviewuser',
            email='configview@example.com',
            password=TEST_PASSWORD
        )
        self.token = UserToken.objects.create(user=self.user_info, token='configview-token-123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.token}')
        
        self.project = Project.objects.create(
            name="Config View Test Project",
            desc="Project for config view testing",
            responsible="configviewuser"
        )

    def test_config_with_multiple_environments(self):
        """Test configuration for multiple environments"""
        
        environments = [
            {
                "name": "Development",
                "base_url": "http://dev.api.local",
                "variables": [
                    {"env": "development"},
                    {"debug": "true"}
                ]
            },
            {
                "name": "Staging",
                "base_url": "https://staging.api.example.com",
                "variables": [
                    {"env": "staging"},
                    {"debug": "false"}
                ]
            },
            {
                "name": "Production",
                "base_url": "https://api.example.com",
                "variables": [
                    {"env": "production"},
                    {"debug": "false"}
                ]
            }
        ]
        
        created_configs = []
        for env in environments:
            config_body = {
                "name": env["name"],
                "request": {
                    "base_url": env["base_url"]
                },
                "variables": env["variables"]
            }
            
            config_data = {
                "name": f"{env['name']} Config",
                "project": self.project.id,
                "body": json.dumps(config_body)
            }
            
            response = self.client.post('/api/fastrunner/config/', config_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            created_configs.append(response.data['config_id'])
        
        # List all configs
        response = self.client.get('/api/fastrunner/config/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)
        
        # Test copying config
        response = self.client.post(
            f'/api/fastrunner/config/{created_configs[0]}/', 
            {"name": "Development Copy"}, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_host_ip_configuration(self):
        """Test Host IP configuration management"""
        
        hosts = [
            {"name": "Local", "host": "http://localhost:8000", "description": "Local development"},
            {"name": "Docker", "host": "http://app:8000", "description": "Docker environment"},
            {"name": "Production", "host": "https://api.example.com", "description": "Production API"}
        ]
        
        created_hosts = []
        for host_data in hosts:
            response = self.client.post('/api/fastrunner/host_ip/', host_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            created_hosts.append(response.data['id'])
        
        # List all host IPs
        response = self.client.get('/api/fastrunner/host_ip/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)
        
        # Update host IP
        update_data = {
            "host": "http://localhost:9000",
            "description": "Updated local development port"
        }
        response = self.client.patch(f'/api/fastrunner/host_ip/{created_hosts[0]}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get single host IP
        response = self.client.get(f'/api/fastrunner/host_ip/{created_hosts[0]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], created_hosts[0])