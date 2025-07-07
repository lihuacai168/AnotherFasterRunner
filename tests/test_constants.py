"""Common test constants and utilities"""
from django.utils.crypto import get_random_string

# Generate a secure random password for tests
TEST_PASSWORD = get_random_string(32)