from django_filters import rest_framework as filters
from tyadmin_api.custom import DateFromToRangeFilter
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from fastrunner.models import Project, Debugtalk, Config, API, Case, CaseStep, HostIP, Variables, Report, ReportDetail, Relation, Visit
from fastuser.models import UserInfo, UserToken, MyUser

class PermissionFilter(filters.FilterSet):
    content_type_text = filters.CharFilter(field_name="content_type")

    class Meta:
        model = Permission
        exclude = []

class GroupFilter(filters.FilterSet):

    class Meta:
        model = Group
        exclude = []

class ContentTypeFilter(filters.FilterSet):

    class Meta:
        model = ContentType
        exclude = []

class ProjectFilter(filters.FilterSet):
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Project
        exclude = []

class DebugtalkFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Debugtalk
        exclude = []

class ConfigFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Config
        exclude = []

class APIFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = API
        exclude = []

class CaseFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Case
        exclude = []

class CaseStepFilter(filters.FilterSet):
    case_text = filters.CharFilter(field_name="case")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = CaseStep
        exclude = []

class HostIPFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = HostIP
        exclude = []

class VariablesFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Variables
        exclude = []

class ReportFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = Report
        exclude = ["ci_metadata"]

class ReportDetailFilter(filters.FilterSet):
    report_text = filters.CharFilter(field_name="report")

    class Meta:
        model = ReportDetail
        exclude = []

class RelationFilter(filters.FilterSet):
    project_text = filters.CharFilter(field_name="project")

    class Meta:
        model = Relation
        exclude = []

class VisitFilter(filters.FilterSet):
    create_time = DateFromToRangeFilter(field_name="create_time")

    class Meta:
        model = Visit
        exclude = []

class UserInfoFilter(filters.FilterSet):
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = UserInfo
        exclude = []

class UserTokenFilter(filters.FilterSet):
    user_text = filters.CharFilter(field_name="user")
    create_time = DateFromToRangeFilter(field_name="create_time")
    update_time = DateFromToRangeFilter(field_name="update_time")

    class Meta:
        model = UserToken
        exclude = []

class MyUserFilter(filters.FilterSet):
    last_login = DateFromToRangeFilter(field_name="last_login")
    date_joined = DateFromToRangeFilter(field_name="date_joined")

    class Meta:
        model = MyUser
        exclude = []