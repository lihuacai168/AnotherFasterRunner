import os
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from fastrunner.utils.runner import EXEC, DebugCode, decode


class TestDebugCode:
    """Test cases for DebugCode class"""

    def test_init(self):
        """Test DebugCode initialization"""
        code = "print('Hello, World!')"
        
        with patch('tempfile.mkdtemp', return_value='/tmp/test_temp') as mock_mkdtemp:
            debug_code = DebugCode(code)
            
            assert debug_code._DebugCode__code == code
            assert debug_code.resp is None
            assert debug_code.temp == '/tmp/test_temp'
            mock_mkdtemp.assert_called_once_with(prefix='FasterRunner')

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_success(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test successful code execution"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        mock_check_output.return_value = b'Hello, World!\n'
        
        code = "print('Hello, World!')"
        debug_code = DebugCode(code)
        
        # Run the code
        debug_code.run()
        
        # Verify calls
        assert mock_chdir.call_count == 2
        mock_chdir.assert_any_call('/tmp/test_temp')
        mock_chdir.assert_any_call(debug_code.run.__globals__['BASE_DIR'])
        
        # Verify file was dumped
        expected_file_path = os.path.join('/tmp/test_temp', 'debugtalk.py')
        mock_dump.assert_called_once_with(expected_file_path, code)
        
        # Verify subprocess call
        mock_check_output.assert_called_once()
        call_args = mock_check_output.call_args
        assert call_args[0][0] == [EXEC, expected_file_path]
        assert call_args[1]['stderr'] == subprocess.STDOUT
        assert call_args[1]['timeout'] == 60
        assert 'env' in call_args[1]
        
        # Verify response
        assert debug_code.resp == 'Hello, World!\n'
        
        # Verify cleanup
        mock_rmtree.assert_called_once_with('/tmp/test_temp')

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_with_error(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test code execution with CalledProcessError"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        error = subprocess.CalledProcessError(1, 'python', output=b'Error: Division by zero')
        mock_check_output.side_effect = error
        
        code = "print(1/0)"
        debug_code = DebugCode(code)
        
        # Run the code
        debug_code.run()
        
        # Verify error handling
        assert debug_code.resp == 'Error: Division by zero'
        
        # Verify cleanup still happens
        mock_rmtree.assert_called_once_with('/tmp/test_temp')

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_with_timeout(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test code execution with timeout"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        mock_check_output.side_effect = subprocess.TimeoutExpired('python', 60)
        
        code = "import time; time.sleep(100)"
        debug_code = DebugCode(code)
        
        # Run the code
        debug_code.run()
        
        # Verify timeout handling
        assert debug_code.resp == 'RunnerTimeOut'
        
        # Verify cleanup still happens
        mock_rmtree.assert_called_once_with('/tmp/test_temp')

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_with_unicode_output(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test code execution with unicode output"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        mock_check_output.return_value = '测试中文输出\n'.encode('utf-8')
        
        code = "print('测试中文输出')"
        debug_code = DebugCode(code)
        
        # Run the code
        debug_code.run()
        
        # Verify unicode handling
        assert debug_code.resp == '测试中文输出\n'

    @patch('fastrunner.utils.runner.sys.path', ['/usr/lib/python3', '/home/user/.local/lib'])
    @patch('fastrunner.utils.runner.BASE_DIR', '/app/FasterRunner')
    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_pythonpath_setup(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test PYTHONPATH environment variable setup"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        mock_check_output.return_value = b'OK'
        
        code = "import sys; print(sys.path)"
        debug_code = DebugCode(code)
        
        # Run the code
        debug_code.run()
        
        # Verify PYTHONPATH was set correctly
        call_args = mock_check_output.call_args[1]
        env = call_args['env']
        pythonpath = env['PYTHONPATH']
        
        # Should include BASE_DIR first, then existing sys.path
        expected_paths = ['/app/FasterRunner', '/usr/lib/python3', '/home/user/.local/lib']
        assert pythonpath == ':'.join(expected_paths)

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_run_exception_during_cleanup(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test handling of exception during cleanup"""
        # Setup mocks
        mock_mkdtemp.return_value = '/tmp/test_temp'
        mock_check_output.return_value = b'OK'
        mock_rmtree.side_effect = OSError("Permission denied")
        
        code = "print('test')"
        debug_code = DebugCode(code)
        
        # Run should raise the cleanup exception
        with pytest.raises(OSError, match="Permission denied"):
            debug_code.run()
        
        # But the response should still be set
        assert debug_code.resp == 'OK'


class TestDecode:
    """Test cases for decode function"""

    def test_decode_utf8_success(self):
        """Test decoding UTF-8 encoded bytes"""
        utf8_bytes = "Hello, 世界!".encode('utf-8')
        result = decode(utf8_bytes)
        assert result == "Hello, 世界!"

    def test_decode_gbk_fallback(self):
        """Test fallback to GBK when UTF-8 fails"""
        # Create bytes that are valid GBK but invalid UTF-8
        # GBK encoding for "中文"
        gbk_bytes = "中文测试".encode('gbk')
        result = decode(gbk_bytes)
        assert result == "中文测试"

    def test_decode_ascii(self):
        """Test decoding plain ASCII"""
        ascii_bytes = b"Hello, World!"
        result = decode(ascii_bytes)
        assert result == "Hello, World!"

    def test_decode_empty_bytes(self):
        """Test decoding empty bytes"""
        result = decode(b"")
        assert result == ""

    def test_decode_with_newlines(self):
        """Test decoding bytes with newlines"""
        bytes_with_newlines = b"Line 1\nLine 2\r\nLine 3"
        result = decode(bytes_with_newlines)
        assert result == "Line 1\nLine 2\r\nLine 3"

    def test_decode_with_special_chars(self):
        """Test decoding bytes with special characters"""
        special_bytes = "Special chars: @#$%^&*()[]{}".encode('utf-8')
        result = decode(special_bytes)
        assert result == "Special chars: @#$%^&*()[]{}"


class TestExecVariable:
    """Test cases for EXEC variable logic"""

    def test_exec_normal_python(self):
        """Test EXEC when using normal Python"""
        with patch('fastrunner.utils.runner.sys.executable', '/usr/bin/python3'):
            # Re-import to get the updated EXEC value
            from fastrunner.utils import runner
            assert '/usr/bin/python3' in runner.EXEC
            assert 'uwsgi' not in runner.EXEC

    def test_exec_with_uwsgi(self):
        """Test EXEC when using uwsgi"""
        with patch('fastrunner.utils.runner.sys.executable', '/usr/bin/uwsgi'):
            # Re-import to get the updated EXEC value
            from fastrunner.utils import runner
            # Should be replaced with python
            assert runner.EXEC == '/usr/bin/python'

    def test_exec_with_uwsgi_in_path(self):
        """Test EXEC when uwsgi is in the path"""
        with patch('fastrunner.utils.runner.sys.executable', '/opt/venv/bin/uwsgi'):
            # Re-import to get the updated EXEC value
            from fastrunner.utils import runner
            # Should replace uwsgi with python
            assert runner.EXEC == '/opt/venv/bin/python'


class TestIntegration:
    """Integration tests for DebugCode"""

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir')
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_complex_code_execution(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test execution of complex Python code"""
        mock_mkdtemp.return_value = '/tmp/test_complex'
        
        # Simulate complex output with multiple encodings
        output = """Result: 42
中文输出: 测试
Error occurred: None
""".encode('utf-8')
        
        mock_check_output.return_value = output
        
        complex_code = """
import json
def calculate():
    return 42

result = calculate()
print(f"Result: {result}")
print("中文输出: 测试")
print(f"Error occurred: {None}")
"""
        
        debug_code = DebugCode(complex_code)
        debug_code.run()
        
        assert "Result: 42" in debug_code.resp
        assert "中文输出: 测试" in debug_code.resp
        assert "Error occurred: None" in debug_code.resp

    @patch('fastrunner.utils.runner.shutil.rmtree')
    @patch('fastrunner.utils.runner.os.chdir') 
    @patch('fastrunner.utils.runner.loader.FileLoader.dump_python_file')
    @patch('subprocess.check_output')
    @patch('tempfile.mkdtemp')
    def test_multiline_error_output(self, mock_mkdtemp, mock_check_output, mock_dump, mock_chdir, mock_rmtree):
        """Test handling of multiline error output"""
        mock_mkdtemp.return_value = '/tmp/test_error'
        
        error_output = b"""Traceback (most recent call last):
  File "debugtalk.py", line 3, in <module>
    result = 1 / 0
ZeroDivisionError: division by zero"""
        
        error = subprocess.CalledProcessError(1, 'python', output=error_output)
        mock_check_output.side_effect = error
        
        code = "result = 1 / 0"
        debug_code = DebugCode(code)
        debug_code.run()
        
        assert "ZeroDivisionError: division by zero" in debug_code.resp
        assert "Traceback" in debug_code.resp