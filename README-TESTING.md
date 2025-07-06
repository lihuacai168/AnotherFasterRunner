# Testing Guide for AnotherFasterRunner

This document provides comprehensive guidance on testing within the AnotherFasterRunner project.

## 📋 Table of Contents
- [Testing Overview](#testing-overview)
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Coverage Requirements](#coverage-requirements)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)

## 🎯 Testing Overview

AnotherFasterRunner uses **pytest** as the primary testing framework with **Django integration**. The testing strategy focuses on:

- **Unit Tests**: Testing individual functions and classes in isolation
- **Integration Tests**: Testing component interactions
- **API Tests**: Testing HTTP endpoints and responses
- **Model Tests**: Testing Django model behavior and constraints

### Current Coverage Status
- **Target Coverage**: 60% minimum (configured in pytest.ini)
- **Current Coverage**: Run `make test-coverage` to see current status
- **Priority Areas**: Models, Views, and Utility functions

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install all dependencies including test dependencies
poetry install

# Or install test dependencies only
make install-test-deps
```

### 2. Run Tests
```bash
# Run all tests with coverage
make test

# Run tests without coverage (faster)
make test-fast

# Run specific test types
make test-unit
make test-integration
```

### 3. View Coverage Report
```bash
# Generate HTML coverage report
make test-coverage

# Open coverage report in browser
open htmlcov/index.html
```

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_models.py           # Model tests
├── test_api_views.py        # API endpoint tests
├── test_utils.py           # Utility function tests
└── test_login_views.py     # Authentication tests

fastrunner/tests/
└── test_tree_service_impl.py  # Service layer tests

Configuration Files:
├── pytest.ini             # Pytest configuration
├── .coveragerc            # Coverage configuration
└── conftest.py           # Global test fixtures
```

## 🔧 Running Tests

### Basic Commands

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_models.py

# Run specific test method
pytest tests/test_models.py::TestProjectModel::test_project_creation

# Run tests with specific markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Exclude slow tests
```

### Using Makefile Commands

```bash
# Most common commands
make test              # All tests with coverage
make test-fast         # All tests without coverage
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-coverage     # Detailed coverage report

# Development commands
make test-watch        # Watch mode for development
make test-specific FILE=test_models.py  # Specific file

# Quality commands
make lint              # Code linting
make lint-fix          # Fix lint issues
make quality           # Lint + tests + coverage
```

## 📊 Coverage Requirements

### Minimum Coverage Targets
- **Overall Project**: 60% minimum (will increase over time)
- **New Code**: 80% minimum for new features
- **Critical Paths**: 90% minimum for security and core business logic

### Coverage Configuration
Coverage settings are configured in `.coveragerc`:

```ini
[run]
source = .
omit = 
    */migrations/*
    */tests/*
    */settings/*
    # ... other exclusions

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    # ... other exclusions
```

### Viewing Coverage Reports

```bash
# Terminal report
pytest --cov-report=term-missing

# HTML report (recommended)
pytest --cov-report=html
open htmlcov/index.html

# XML report (for CI)
pytest --cov-report=xml
```

## ✍️ Writing Tests

### Test File Organization

1. **Location**: Place tests in the `tests/` directory
2. **Naming**: Use `test_*.py` pattern
3. **Structure**: Mirror the application structure

### Basic Test Structure

```python
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase

@pytest.mark.django_db
class TestModelName(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create test objects
        pass
        
    def test_basic_functionality(self):
        """Test basic model functionality"""
        # Arrange
        # Act  
        # Assert
        assert True
```

### Available Fixtures

Common fixtures are available in `conftest.py`:

```python
def test_with_authenticated_user(authenticated_user):
    """Test using authenticated user fixture"""
    assert authenticated_user.username == 'testuser'

def test_with_api_client(authenticated_client):
    """Test using authenticated API client"""
    response = authenticated_client.get('/api/projects/')
    assert response.status_code == 200

def test_with_sample_data(sample_project, sample_api):
    """Test using sample project and API data"""
    assert sample_api.project == sample_project
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_function():
    """Fast unit test"""
    pass

@pytest.mark.integration  
def test_integration_feature():
    """Integration test"""
    pass

@pytest.mark.slow
def test_expensive_operation():
    """Slow test (e.g., external API calls)"""
    pass
```

### Testing Best Practices

1. **AAA Pattern**: Arrange, Act, Assert
2. **One Assertion**: One logical assertion per test
3. **Descriptive Names**: Clear test method names
4. **Independent Tests**: Each test should be independent
5. **Mock External Dependencies**: Use mocks for external services

### Example Test Cases

#### Model Tests
```python
@pytest.mark.django_db
class TestProjectModel(TestCase):
    
    def test_project_creation(self):
        """Test basic project creation"""
        project = Project.objects.create(
            name="Test Project",
            desc="Test Description",
            responsible="testuser"
        )
        assert project.name == "Test Project"
        assert project.is_deleted == 0
```

#### API Tests
```python
@pytest.mark.django_db
class TestProjectAPI(APITestCase):
    
    def test_project_list_requires_authentication(self):
        """Test that project list requires authentication"""
        response = self.client.get('/api/projects/')
        assert response.status_code == 401
```

#### Utility Tests
```python
class TestTreeUtils:
    
    def test_get_tree_max_id_empty(self):
        """Test get_tree_max_id with empty tree"""
        result = get_tree_max_id([])
        assert result == 0
```

## 🔄 CI/CD Integration

### GitHub Actions Configuration

Add this to `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install Poetry
      uses: snok/install-poetry@v1
      
    - name: Install dependencies
      run: poetry install
      
    - name: Run tests
      run: make ci-test
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: tests
        entry: make test-fast
        language: system
        pass_filenames: false
        always_run: true
```

## 🛠️ Development Workflow

### Adding New Tests

1. **Create Test File**: Follow naming convention `test_*.py`
2. **Write Test Cases**: Cover happy path, edge cases, and error conditions
3. **Run Tests**: Ensure they pass locally
4. **Check Coverage**: Ensure adequate coverage
5. **Commit**: Include tests with feature commits

### Test-Driven Development (TDD)

```bash
# 1. Write failing test
pytest tests/test_new_feature.py::test_new_functionality -v

# 2. Implement minimum code to pass
# ... write code ...

# 3. Run test again
pytest tests/test_new_feature.py::test_new_functionality -v

# 4. Refactor and ensure tests still pass
make test
```

### Debugging Tests

```bash
# Run with verbose output
pytest -v

# Run with print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Run last failed tests only
pytest --lf
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing Documentation](https://www.django-rest-framework.org/api-guide/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `PYTHONPATH` includes project root
2. **Database Issues**: Use `@pytest.mark.django_db` decorator
3. **Fixture Not Found**: Check `conftest.py` imports
4. **Coverage Too Low**: Add tests for untested code paths

### Getting Help

1. Check test logs: `pytest -v --tb=short`
2. Review coverage report: `open htmlcov/index.html`
3. Run specific test: `pytest tests/test_file.py::test_method -v`

---

**Remember**: Good tests are an investment in code quality and maintainability. Write tests that would help you understand the code six months from now!