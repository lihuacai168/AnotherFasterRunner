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
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.static import serve
from fastrunner.views import run_all_auto_case
from FasterRunner.settings.docker import STATIC_ROOT, MEDIA_ROOT
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_jwt.views import obtain_jwt_token
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
    authentication_classes=[],
)

urlpatterns = [
    path(r"login", obtain_jwt_token),
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    url(r'^docs/', schema_view, name="docs"),
    url(r'^accounts/', include('rest_framework.urls',)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework_api_auth')),
    path('api/user/', include('fastuser.urls')),
    path('api/fastrunner/', include('fastrunner.urls')),

    # 执行定时任务
    # TODO 需要增加触发检验，暂时关闭触发入口
    # re_path(r'^run_all_auto_case/$', run_all_auto_case.run_all_auto_case, name='run_all_auto_case'),
    re_path(r'^get_report_url/$', run_all_auto_case.get_report_url, name='get_report_url'),

    # swagger
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
