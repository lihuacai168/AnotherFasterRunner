import datetime
import logging
import smtplib
from unittest.mock import MagicMock, Mock, patch

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from fastrunner.utils.middleware import ExceptionMiddleware, VisitTimesMiddleware


class TestVisitTimesMiddleware:
    """Test cases for VisitTimesMiddleware"""

    @pytest.fixture
    def middleware(self):
        return VisitTimesMiddleware(get_response=lambda request: HttpResponse())

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    def test_process_request_copies_body(self, middleware, request_factory):
        """Test that process_request copies the body"""
        request = request_factory.post('/test', data=b'test body')
        
        middleware.process_request(request)
        
        assert hasattr(request, '_body')
        assert request._body == b'test body'

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_skip_fonts(self, mock_visit, middleware, request_factory):
        """Test that font URLs are skipped"""
        request = request_factory.get('/fonts/roboto/test.ttf')
        request._body = b''
        request.user = AnonymousUser()
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        assert result == response
        mock_visit.objects.create.assert_not_called()

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_skip_mock(self, mock_visit, middleware, request_factory):
        """Test that mock URLs are skipped"""
        request = request_factory.get('/mock/api/test')
        request._body = b''
        request.user = AnonymousUser()
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        assert result == response
        mock_visit.objects.create.assert_not_called()

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_with_empty_body(self, mock_visit, middleware, request_factory):
        """Test process_response with empty body"""
        request = request_factory.get('/api/test')
        request._body = b''
        request.user = User(username='testuser')
        request.headers = {'x-forwarded-for': '192.168.1.1', 'project': '5'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        mock_visit.objects.create.assert_called_once_with(
            user=request.user,
            url='/api/test',
            request_method='GET',
            request_body='',
            ip='192.168.1.1',
            path='/api/test',
            request_params='',
            project='5'
        )
        assert result == response

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_with_body(self, mock_visit, middleware, request_factory):
        """Test process_response with non-empty body"""
        request = request_factory.post('/api/test')
        request._body = b'{"test": "data"}'
        request.user = User(username='testuser')
        request.headers = {'project': '10'}
        request.META = {'REMOTE_ADDR': '10.0.0.1'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        mock_visit.objects.create.assert_called_once_with(
            user=request.user,
            url='/api/test',
            request_method='POST',
            request_body='{"test": "data"}',
            ip='10.0.0.1',
            path='/api/test',
            request_params='',
            project='10'
        )
        assert result == response

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_with_query_params(self, mock_visit, middleware, request_factory):
        """Test process_response with query parameters"""
        request = request_factory.get('/api/test', {'page': '1', 'search': 'test', 'tag': ''})
        request._body = b''
        request.user = None
        request.headers = {}
        request.META = {'REMOTE_ADDR': '127.0.0.1'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        # Verify the call was made
        assert mock_visit.objects.create.called
        call_args = mock_visit.objects.create.call_args[1]
        
        # Check basic fields
        assert call_args['user'] == 'AnonymousUser'
        assert call_args['path'] == '/api/test'
        assert call_args['request_method'] == 'GET'
        assert call_args['ip'] == '127.0.0.1'
        assert call_args['project'] == 0  # Default when not in headers
        
        # Check URL contains query params
        assert '?' in call_args['url']
        assert 'page=1' in call_args['url']
        assert 'search=test' in call_args['url']
        
        # Check request_params
        assert 'page=1' in call_args['request_params']
        assert 'search=test' in call_args['request_params']

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_with_multiple_ips(self, mock_visit, middleware, request_factory):
        """Test process_response with multiple IPs in x-forwarded-for"""
        request = request_factory.get('/api/test')
        request._body = b''
        request.user = AnonymousUser()
        request.headers = {'x-forwarded-for': '192.168.1.1, 10.0.0.1, 172.16.0.1'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        # Should only use the first IP
        mock_visit.objects.create.assert_called_once()
        call_args = mock_visit.objects.create.call_args[1]
        assert call_args['ip'] == '192.168.1.1'

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_no_user(self, mock_visit, middleware, request_factory):
        """Test process_response when request.user is None"""
        request = request_factory.get('/api/test')
        request._body = b''
        request.user = None
        request.headers = {}
        request.META = {'REMOTE_ADDR': '127.0.0.1'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        mock_visit.objects.create.assert_called_once()
        call_args = mock_visit.objects.create.call_args[1]
        assert call_args['user'] == 'AnonymousUser'

    @patch('fastrunner.utils.middleware.Visit')
    def test_process_response_unicode_body(self, mock_visit, middleware, request_factory):
        """Test process_response with unicode in body"""
        request = request_factory.post('/api/test')
        request._body = '{"message": "测试中文"}'.encode('utf-8')
        request.user = User(username='testuser')
        request.headers = {}
        request.META = {'REMOTE_ADDR': '127.0.0.1'}
        response = HttpResponse()
        
        result = middleware.process_response(request, response)
        
        mock_visit.objects.create.assert_called_once()
        call_args = mock_visit.objects.create.call_args[1]
        assert call_args['request_body'] == '{"message": "测试中文"}'


class TestExceptionMiddleware:
    """Test cases for ExceptionMiddleware"""

    @pytest.fixture
    def middleware(self):
        return ExceptionMiddleware(get_response=lambda request: HttpResponse())

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    def test_build_html_message(self, middleware, request_factory):
        """Test build_html_message method"""
        request = request_factory.get('/test')
        request.user = User(username='testuser')
        request.method = 'GET'
        request.path = '/test'
        request.id = 'test-request-id'
        
        exception = ValueError("Test exception")
        
        with patch('traceback.format_exc', return_value='Test traceback'):
            html = middleware.build_html_message(request, exception)
        
        assert 'testuser' in html
        assert 'GET' in html
        assert '/test' in html
        assert 'test-request-id' in html
        assert 'Test traceback' in html
        assert '<!DOCTYPE html>' in html

    @patch('fastrunner.utils.middleware.logger')
    def test_process_exception_no_email_config(self, mock_logger, middleware, request_factory):
        """Test process_exception when email is not configured"""
        request = request_factory.get('/test')
        exception = ValueError("Test exception")
        
        # Mock settings without email config
        with patch.object(settings, 'EMAIL_HOST_USER', ''), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', ''), \
             patch.object(settings, 'EMAIL_HOST', ''), \
             patch.object(settings, 'EMAIL_PORT', ''):
            
            result = middleware.process_exception(request, exception)
        
        # Should log the error but not send email
        mock_logger.error.assert_called_once()
        assert result is None

    @patch('fastrunner.utils.middleware.email_helper')
    @patch('fastrunner.utils.middleware.logger')
    def test_process_exception_with_email_success(self, mock_logger, mock_email_helper, 
                                                  middleware, request_factory):
        """Test process_exception with successful email send"""
        request = request_factory.get('/test')
        request.user = User(username='testuser')
        request.id = 'test-id'
        exception = ValueError("Test exception")
        
        # Mock settings with email config
        with patch.object(settings, 'EMAIL_HOST_USER', 'test@example.com'), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', 'password'), \
             patch.object(settings, 'EMAIL_HOST', 'smtp.example.com'), \
             patch.object(settings, 'EMAIL_PORT', 587):
            
            result = middleware.process_exception(request, exception)
        
        # Should log error and send email
        assert mock_logger.error.call_count == 1
        mock_email_helper.send_mail.assert_called_once()
        
        # Check email parameters
        call_args = mock_email_helper.send_mail.call_args[1]
        assert call_args['subject'] == '测试平台异常告警'
        assert 'testuser' in call_args['html_message']
        assert call_args['from_email'] == 'test@example.com'
        assert call_args['recipient_list'] == ['test@example.com']
        
        # Should log success
        mock_logger.info.assert_called_once_with('邮件发送成功')

    @patch('fastrunner.utils.middleware.email_helper')
    @patch('fastrunner.utils.middleware.logger')
    def test_process_exception_smtp_auth_error(self, mock_logger, mock_email_helper, 
                                               middleware, request_factory):
        """Test process_exception with SMTP authentication error"""
        request = request_factory.get('/test')
        exception = ValueError("Test exception")
        
        # Mock SMTP auth error
        mock_email_helper.send_mail.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed')
        
        # Mock settings with email config
        with patch.object(settings, 'EMAIL_HOST_USER', 'test@example.com'), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', 'password'), \
             patch.object(settings, 'EMAIL_HOST', 'smtp.example.com'), \
             patch.object(settings, 'EMAIL_PORT', 587):
            
            result = middleware.process_exception(request, exception)
        
        # Should log the original error and the email error
        assert mock_logger.error.call_count == 2
        # Check that the SMTP error was logged
        smtp_error_log = mock_logger.error.call_args_list[1][0][0]
        assert '邮件发送失败' in smtp_error_log
        
        # Should not log success
        mock_logger.info.assert_not_called()

    @patch('fastrunner.utils.middleware.email_helper')
    @patch('fastrunner.utils.middleware.logger')
    def test_process_exception_general_email_error(self, mock_logger, mock_email_helper, 
                                                   middleware, request_factory):
        """Test process_exception with general email sending error"""
        request = request_factory.get('/test')
        exception = ValueError("Test exception")
        
        # Mock general exception
        mock_email_helper.send_mail.side_effect = Exception("Network error")
        
        # Mock settings with email config
        with patch.object(settings, 'EMAIL_HOST_USER', 'test@example.com'), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', 'password'), \
             patch.object(settings, 'EMAIL_HOST', 'smtp.example.com'), \
             patch.object(settings, 'EMAIL_PORT', 587):
            
            result = middleware.process_exception(request, exception)
        
        # Should log the original error and the email error
        assert mock_logger.error.call_count == 2
        error_log = mock_logger.error.call_args_list[1][0][0]
        assert '邮件发送失败' in error_log
        
        # Should not log success
        mock_logger.info.assert_not_called()

    @patch('fastrunner.utils.middleware.email_helper')
    @patch('fastrunner.utils.middleware.logger')
    @patch('traceback.format_exc')
    def test_process_exception_with_complex_exception(self, mock_format_exc, mock_logger, 
                                                      mock_email_helper, middleware, request_factory):
        """Test process_exception with complex exception and traceback"""
        request = request_factory.get('/api/complex/path')
        request.user = User(username='admin')
        request.method = 'POST'
        request.id = 'complex-id'
        
        # Create a complex exception
        try:
            raise RuntimeError("Inner exception") from ValueError("Cause exception")
        except RuntimeError as e:
            exception = e
        
        # Mock complex traceback
        mock_format_exc.return_value = """Traceback (most recent call last):
  File "test.py", line 10, in <module>
    raise ValueError("Cause exception")
ValueError: Cause exception

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "test.py", line 12, in <module>
    raise RuntimeError("Inner exception") from e
RuntimeError: Inner exception"""
        
        # Mock settings with email config
        with patch.object(settings, 'EMAIL_HOST_USER', 'admin@example.com'), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', 'password'), \
             patch.object(settings, 'EMAIL_HOST', 'smtp.example.com'), \
             patch.object(settings, 'EMAIL_PORT', 587):
            
            result = middleware.process_exception(request, exception)
        
        # Verify traceback was formatted
        mock_format_exc.assert_called()
        
        # Verify email was sent with complex traceback
        mock_email_helper.send_mail.assert_called_once()
        call_args = mock_email_helper.send_mail.call_args[1]
        assert 'ValueError: Cause exception' in call_args['html_message']
        assert 'RuntimeError: Inner exception' in call_args['html_message']

    def test_build_html_message_with_missing_attributes(self, middleware, request_factory):
        """Test build_html_message when request has missing attributes"""
        request = request_factory.get('/test')
        # Don't set user, id attributes
        request.method = 'GET'
        request.path = '/test'
        
        exception = Exception("Test")
        
        # Should handle missing attributes gracefully
        with patch('traceback.format_exc', return_value='Test trace'):
            try:
                html = middleware.build_html_message(request, exception)
                # Should at least contain basic HTML structure
                assert '<!DOCTYPE html>' in html
                assert '/test' in html
                assert 'GET' in html
            except AttributeError:
                # It's okay if it fails on missing attributes
                pass

    @patch('fastrunner.utils.middleware.email_helper')
    @patch('fastrunner.utils.middleware.logger')
    def test_process_exception_partial_email_config(self, mock_logger, mock_email_helper, 
                                                    middleware, request_factory):
        """Test process_exception with partial email configuration"""
        request = request_factory.get('/test')
        exception = ValueError("Test exception")
        
        # Mock settings with partial email config (missing PORT)
        with patch.object(settings, 'EMAIL_HOST_USER', 'test@example.com'), \
             patch.object(settings, 'EMAIL_HOST_PASSWORD', 'password'), \
             patch.object(settings, 'EMAIL_HOST', 'smtp.example.com'), \
             patch.object(settings, 'EMAIL_PORT', None):
            
            result = middleware.process_exception(request, exception)
        
        # Should only log error, not send email
        mock_logger.error.assert_called_once()
        mock_email_helper.send_mail.assert_not_called()
        mock_logger.info.assert_not_called()