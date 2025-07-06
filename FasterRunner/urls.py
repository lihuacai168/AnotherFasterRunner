"""FasterRunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from fastrunner.views import run_all_auto_case
from mock.views import MockAPILogViewSet, MockAPIView, MockAPIViewset, MockProjectViewSet
from system import views as system_views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
    authentication_classes=[],
)
system_router = DefaultRouter()
system_router.register(r"log_records", system_views.LogRecordViewSet)

mock_api_router = DefaultRouter()
mock_api_router.register(r"mock_api", MockAPIViewset)


mock_project_router = DefaultRouter()
mock_project_router.register(r"mock_project", MockProjectViewSet)
mock_project_router.register(r"mock_log", MockAPILogViewSet)

urlpatterns = [
    path("api/mock/", include(mock_project_router.urls)),
    path("api/mock/", include(mock_api_router.urls)),
    path(r"login", obtain_jwt_token),
    path("admin/", admin.site.urls),
    # re_path(r'^docs/', schema_view, name="docs"),
    path(
        "accounts/",
        include(
            "rest_framework.urls",
        ),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework_api_auth")),
    path("api/user/", include("fastuser.urls")),
    path("api/fastrunner/", include("fastrunner.urls")),
    path("api/system/", include(system_router.urls)),
    # 执行定时任务
    # TODO 需要增加触发检验，暂时关闭触发入口
    # re_path(r'^run_all_auto_case/$', run_all_auto_case.run_all_auto_case, name='run_all_auto_case'),
    path("get_report_url/", run_all_auto_case.get_report_url, name="get_report_url"),
    # swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r'^mock/(?P<project_id>\w+)(?P<path>/.*)$', MockAPIView.as_view())
]
