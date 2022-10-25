"""
Django settings for FasterRunner project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.db.models import AutoField
import datetime as datetime
from loguru import logger

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "e$od9f28jce8q47u3raik$(e%$@lff6r89ux+=f!e1a$e42+#7"

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Token Settings, 30天过期
INVALID_TIME = 60 * 60 * 24 * 3650

# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fastrunner.apps.FastrunnerConfig",
    "fastuser",
    "rest_framework",
    "corsheaders",
    # 'djcelery',
    "django_celery_beat",
    "rest_framework_swagger",
    "drf_yasg",
    "captcha", "tyadmin_api_cli", "tyadmin_api"
]

TY_ADMIN_CONFIG = {
    'GEN_APPS': ['fastuser', 'fastrunner']
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "fastrunner.utils.middleware.VisitTimesMiddleware",
]

ROOT_URLCONF = "FasterRunner.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 'DIRS': [os.path.join(BASE_DIR, '../../templates')],
        "DIRS": [os.path.join(BASE_DIR, "./templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "FasterRunner.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-valid

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Define MEDIA_URL as the base public URL of that directory. Make sure that this directory is writable by the Web
# server's user account. Define MEDIA_ROOT as the full path to a directory where you'd like Django to store uploaded
# files. (For performance, these files are not stored in the database.)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': ['FasterRunner.auth.DeleteAuthenticator', 'FasterRunner.auth.Authenticator', ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "FasterRunner.auth.MyJWTAuthentication",
        # 'FasterRunner.auth.DeleteAuthenticator',
        # 'FasterRunner.auth.Authenticator',
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
    # json form 渲染
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "FasterRunner.pagination.MyPageNumberPagination",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}
JWT_AUTH = {
    # 'JWT_SECRET_KEY': SECRET_KEY,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=365),
    "JWT_ALLOW_REFRESH": True,
}
AUTH_USER_MODEL = "fastuser.MyUser"

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "FasterRunner.swagger.CustomSwaggerAutoSchema",
    # 基础样式
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    # 'LOGIN_URL': 'rest_framework:login',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    "APIS_SORTER": "alpha",
    # 如果支持json提交, 则接口文档中包含json输入框
    "JSON_EDITOR": True,
    # 方法列表字母排序
    "OPERATIONS_SORTER": "alpha",
    "VALIDATOR_URL": None,
}
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    # '*',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:8888',
    'http://localhost:8888',
)

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "VIEW",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Project",
)
MQ_USER = "admin"
MQ_PASSWORD = "111111"
HOST = "localhost"
DB_NAME = "faster_db"

IM_REPORT_SETTING = {
    "base_url": "http://10.129.144.24",
    "port": 8000,
    "report_title": "自动化测试报告",
}

for level in ["INFO", "WARNING", "ERROR"]:
    logger.add(
        f"logs/{level.lower()}.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS}"
        " [pid:{process} -> thread:{thread.name}]"
        " {level}"
        " [{name}:{function}:{line}]"
        " {message}",
        level=level,
        rotation="00:00",
        retention="14 days",
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
        # 日志格式
    },
    "filters": {},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            # 'filename': os.path.join(BASE_DIR, 'logs/../../logs/debug.log'),
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "maxBytes": 1024 * 1024 * 50,
            "backupCount": 5,
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "request_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            # 'filename': os.path.join(BASE_DIR, 'logs/../../logs/run.log'),
            "filename": os.path.join(BASE_DIR, "logs/run.log"),
            "maxBytes": 1024 * 1024 * 50,
            "backupCount": 5,
            "formatter": "standard",
        },
        "scprits_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            # 'filename': os.path.join(BASE_DIR, 'logs/../../logs/run.log'),
            "filename": os.path.join(BASE_DIR, "logs/run.log"),
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["default", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "FasterRunner.app": {
            "handlers": ["default", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["request_handler"],
            "level": "INFO",
            "propagate": True,
        },
        "FasterRunner": {
            "handlers": ["scprits_handler", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# https://github.com/celery/celery/issues/4796
DJANGO_CELERY_BEAT_TZ_AWARE = False
