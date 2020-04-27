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
from django.conf.urls import url
from django.urls import path, include, re_path
from fastrunner.views import timer_task, run_all_auto_case, api_rig, api_provide_to_nodejs

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
                              permission_classes=[], authentication_classes=[])


from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path(r"login", obtain_jwt_token),
    path('admin/', admin.site.urls),
    url(r'^docs/', schema_view, name="docs"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/', include('fastuser.urls')),
    path('api/fastrunner/', include('fastrunner.urls')),
    re_path(r'^auto_run_testsuite_pk/$', timer_task.auto_run_testsuite_pk, name='auto_run_testsuite_pk'),
    re_path(r'^run_all_auto_case/$', run_all_auto_case.run_all_auto_case, name='run_all_auto_case'),
    # 网关rig更新API接口 http://localhost:8000/api_rig/200008/?token=5b9c762514728ef01b1cc9f05e8ba74e
    path('api_rig/<int:rig_id>/', api_rig.APIRigView.as_view({"patch": "update"})),
    # 网关rig增加API接口 http://localhost:8000/api_rig/?token=5b9c762514728ef01b1cc9f05e8ba74e
    path('api_rig/', api_rig.APIRigView.as_view({"post": "add"})),
    path('api_provide_to_nodejs/', api_provide_to_nodejs.APIRigView.as_view({"get": "list"})),
]
