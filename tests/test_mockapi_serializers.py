import ast
import textwrap

from django.test import TestCase
from rest_framework import serializers

from mock.serializers import MockAPISerializer


class TestMockAPISerializer(TestCase):
    def setUp(self):
        """
        This will run before every test method.
        """
        self.serializer = MockAPISerializer()

    def test_invalid_response_text(self):
        # Checking invalid response text
        invalid_response_text = "invalid code"
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_response_text(invalid_response_text)

    def test_response_text_no_execute(self):
        # Checking a response text with no 'execute' function
        response_text_no_execute = """
def other_function():
    pass
"""
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_response_text(response_text_no_execute)

    def test_response_text_bad_execute(self):
        # Checking response text with incorrect 'execute' function arguments
        response_text_bad_execute = """
def execute(a, b, c):
    pass
"""
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_response_text(response_text_bad_execute)

    def test_valid_response_text(self):
        # Checking valid response text
        valid_response_text = """
def execute(req, resp):
    pass
"""
        self.assertEqual(
            valid_response_text,
            self.serializer.validate_response_text(valid_response_text),
        )

    def test_indent_error_text(self):
        # Checking response text with incorrect indentation
        indent_error_text = """
 def execute(req, resp):
    a = '1'
"""
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_response_text(indent_error_text)