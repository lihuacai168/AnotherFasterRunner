# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AnotherFasterRunner (FasterRunner) is a Django-based API testing platform that simplifies interface testing and automation. It supports HTTP(S) interface testing, test case parameterization, hook mechanisms, and integration with CI/CD tools.

## Common Development Commands

### Quick Start (Docker)
```bash
# One-command deployment with all services
make fastup  # or just 'make'

# Start services with specific docker-compose file
make up                    # Uses docker-compose.yml
make up-no-build          # Start without rebuilding images
make down                 # Stop all services
make logs                 # View logs for app, celery, web, nginx
make restart service=app  # Restart specific service
make exec service=app     # Shell into service container
```

### Python Development
```bash
# Install dependencies (project uses Poetry)
poetry install

# Run tests
pytest                          # Run all tests
pytest tests/test_login_views.py  # Run specific test file
pytest -k "test_name"           # Run tests matching pattern

# Linting and formatting
poetry run ruff check .         # Run linter
poetry run ruff check --fix .   # Auto-fix linting issues

# Django management commands
python manage.py runserver      # Run development server
python manage.py migrate        # Apply database migrations
python manage.py makemigrations # Create new migrations
python manage.py createsuperuser # Create admin user
```

### Frontend Development
```bash
cd web
npm install          # Install dependencies
npm run dev         # Run development server
npm run build       # Build for production
```

## High-Level Architecture

### Project Structure
- **FasterRunner/**: Main Django project settings with environment-specific configs (base, dev, docker, pro)
- **fastrunner/**: Core app containing API testing functionality
  - Models define test cases, projects, configs, reports
  - Views organized by feature: project, api, run, schedule, etc.
  - Services layer for business logic separation
  - Utils for helpers and shared functionality
- **httprunner/**: Custom HTTP testing engine based on Python Requests
- **fastuser/**: User authentication and management
- **mock/**: Mock server functionality for API simulation
- **system/**: System monitoring and logging features
- **web/**: Vue.js 2.5.2 frontend with Element UI

### Service Architecture
The application runs as microservices via Docker:
- **app**: Django application server (uWSGI)
- **celery-worker**: Async task processing
- **celery-beat**: Scheduled task runner
- **nginx**: Reverse proxy and static file serving
- **mysql**: Database (MySQL/MariaDB)
- **rabbitmq**: Message broker for Celery

### Key Technologies
- Backend: Django 4.1.13 + Django REST Framework 3.14.0
- Authentication: JWT tokens via djangorestframework-jwt
- Task Queue: Celery 5.2.7 with RabbitMQ
- Frontend: Vue.js 2.5.2 with Element UI 2.15.13
- Testing Engine: Custom httprunner module
- Python: 3.11+ (tested on 3.9, 3.10, 3.11)

### Testing Approach
The platform supports:
- HTTP(S) interface testing with parameterization
- Test case dependencies via hook mechanisms
- Integration with YAPI/Swagger/Postman
- Scheduled test execution via crontab
- Test reports with notifications (DingTalk, Lark, Enterprise WeChat)

### Environment Configuration
- Settings in `FasterRunner/settings/` for different environments
- Docker configs: `docker-compose.yml`, `docker-compose-for-fastup.yml`
- Environment variables via `.env` files
- Makefile supports ENV_FILE parameter for custom env files

### Database Models
Key models in fastrunner:
- Project: Test project organization
- API: Individual API definitions
- Case/CaseStep: Test cases and steps
- Config: Environment configurations
- Report: Test execution reports
- Variables: Global and project variables