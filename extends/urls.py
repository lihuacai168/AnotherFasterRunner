"""FasterRunner URL n

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
from django.urls import path

from extends import views

urlpatterns = [
    path('project/<int:id>/schedule', views.Task.as_view({
        "get": "list",
        "post": "add_job"
    })),
    path('project/<int:id>/schedule/<int:schedule_id>', views.Task.as_view({
        "get": "run_once",
        "delete": "delete_job",
        "post": "modify_job"
    })),
    path('schedule/task/<int:pk>', views.Task.as_view({
        "get": "runonce"
    })),
    path('users', views.Task.as_view({
        "get": "get_users"
    })),
    path('test/<int:id>/locust', views.LocustEnv.as_view({
        "put": "add_locust_env",
        "delete": "remove_locust_env"
    })),
    path('project/<int:id>/locust', views.LocustEnv.as_view({
        "get": "get_locust_envs",
    })),
    path('project/<int:id>/reports', views.Report.as_view({
        "get": "list"
    })),
    path('project/<int:id>/report', views.Report.as_view({
        "get": "get_reports"
    })),
    path('project/<int:id>/postman/<int:type>/upload', views.tansfer_postman_to_httprunner)

]
