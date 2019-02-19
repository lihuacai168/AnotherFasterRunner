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

from django.urls import path, include, re_path
from fastrunner.views import timer_task,run_all_auto_case
urlpatterns = [
    path('api/user/', include('fastuser.urls')),
    path('api/fastrunner/', include('fastrunner.urls')),
    re_path(r'^auto_run_testsuite_pk/$', timer_task.auto_run_testsuite_pk, name='auto_run_testsuite_pk'),
    re_path(r'^run_all_auto_case/$', run_all_auto_case.run_all_auto_case, name='run_all_auto_case'),

]
