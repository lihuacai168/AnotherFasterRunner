
from rest_framework import viewsets
from tyadmin_api.custom import XadminViewSet
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from fastrunner.models import Project, Debugtalk, Config, API, Case, CaseStep, HostIP, Variables, Report, ReportDetail, Relation, Visit
from fastuser.models import UserInfo, UserToken, MyUser

from tyadmin_api.auto_serializers import PermissionListSerializer, GroupListSerializer, ContentTypeListSerializer, ProjectListSerializer, DebugtalkListSerializer, ConfigListSerializer, APIListSerializer, CaseListSerializer, CaseStepListSerializer, HostIPListSerializer, VariablesListSerializer, ReportListSerializer, ReportDetailListSerializer, RelationListSerializer, VisitListSerializer, UserInfoListSerializer, UserTokenListSerializer, MyUserListSerializer
from tyadmin_api.auto_serializers import PermissionCreateUpdateSerializer, GroupCreateUpdateSerializer, ContentTypeCreateUpdateSerializer, ProjectCreateUpdateSerializer, DebugtalkCreateUpdateSerializer, ConfigCreateUpdateSerializer, APICreateUpdateSerializer, CaseCreateUpdateSerializer, CaseStepCreateUpdateSerializer, HostIPCreateUpdateSerializer, VariablesCreateUpdateSerializer, ReportCreateUpdateSerializer, ReportDetailCreateUpdateSerializer, RelationCreateUpdateSerializer, VisitCreateUpdateSerializer, UserInfoCreateUpdateSerializer, UserTokenCreateUpdateSerializer, MyUserCreateUpdateSerializer
from tyadmin_api.auto_filters import PermissionFilter, GroupFilter, ContentTypeFilter, ProjectFilter, DebugtalkFilter, ConfigFilter, APIFilter, CaseFilter, CaseStepFilter, HostIPFilter, VariablesFilter, ReportFilter, ReportDetailFilter, RelationFilter, VisitFilter, UserInfoFilter, UserTokenFilter, MyUserFilter

    
class PermissionViewSet(XadminViewSet):
    serializer_class = PermissionListSerializer
    queryset = Permission.objects.all().order_by('-pk')
    filter_class = PermissionFilter
    search_fields = ["name","codename"]

    def get_serializer_class(self):
        if self.action == "list":
            return PermissionListSerializer
        else:
            return PermissionCreateUpdateSerializer

    
class GroupViewSet(XadminViewSet):
    serializer_class = GroupListSerializer
    queryset = Group.objects.all().order_by('-pk')
    filter_class = GroupFilter
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return GroupListSerializer
        else:
            return GroupCreateUpdateSerializer

    
class ContentTypeViewSet(XadminViewSet):
    serializer_class = ContentTypeListSerializer
    queryset = ContentType.objects.all().order_by('-pk')
    filter_class = ContentTypeFilter
    search_fields = ["app_label","model"]

    def get_serializer_class(self):
        if self.action == "list":
            return ContentTypeListSerializer
        else:
            return ContentTypeCreateUpdateSerializer

    
class ProjectViewSet(XadminViewSet):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all().order_by('-pk')
    filter_class = ProjectFilter
    search_fields = ["creator","updater","name","desc","responsible","yapi_base_url","yapi_openapi_token","jira_project_key","jira_bearer_token"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        else:
            return ProjectCreateUpdateSerializer

    
class DebugtalkViewSet(XadminViewSet):
    serializer_class = DebugtalkListSerializer
    queryset = Debugtalk.objects.all().order_by('-pk')
    filter_class = DebugtalkFilter
    search_fields = ["creator","updater"]

    def get_serializer_class(self):
        if self.action == "list":
            return DebugtalkListSerializer
        else:
            return DebugtalkCreateUpdateSerializer

    
class ConfigViewSet(XadminViewSet):
    serializer_class = ConfigListSerializer
    queryset = Config.objects.all().order_by('-pk')
    filter_class = ConfigFilter
    search_fields = ["creator","updater","name","base_url"]

    def get_serializer_class(self):
        if self.action == "list":
            return ConfigListSerializer
        else:
            return ConfigCreateUpdateSerializer

    
class APIViewSet(XadminViewSet):
    serializer_class = APIListSerializer
    queryset = API.objects.all().order_by('-pk')
    filter_class = APIFilter
    search_fields = ["creator","updater","name","url","method","ypai_add_time","ypai_up_time","ypai_username"]

    def get_serializer_class(self):
        if self.action == "list":
            return APIListSerializer
        else:
            return APICreateUpdateSerializer

    
class CaseViewSet(XadminViewSet):
    serializer_class = CaseListSerializer
    queryset = Case.objects.all().order_by('-pk')
    filter_class = CaseFilter
    search_fields = ["creator","updater","name"]

    def get_serializer_class(self):
        if self.action == "list":
            return CaseListSerializer
        else:
            return CaseCreateUpdateSerializer

    
class CaseStepViewSet(XadminViewSet):
    serializer_class = CaseStepListSerializer
    queryset = CaseStep.objects.all().order_by('-pk')
    filter_class = CaseStepFilter
    search_fields = ["creator","updater","name","url","method"]

    def get_serializer_class(self):
        if self.action == "list":
            return CaseStepListSerializer
        else:
            return CaseStepCreateUpdateSerializer

    
class HostIPViewSet(XadminViewSet):
    serializer_class = HostIPListSerializer
    queryset = HostIP.objects.all().order_by('-pk')
    filter_class = HostIPFilter
    search_fields = ["creator","updater","name"]

    def get_serializer_class(self):
        if self.action == "list":
            return HostIPListSerializer
        else:
            return HostIPCreateUpdateSerializer

    
class VariablesViewSet(XadminViewSet):
    serializer_class = VariablesListSerializer
    queryset = Variables.objects.all().order_by('-pk')
    filter_class = VariablesFilter
    search_fields = ["creator","updater","key","value","description"]

    def get_serializer_class(self):
        if self.action == "list":
            return VariablesListSerializer
        else:
            return VariablesCreateUpdateSerializer

    
class ReportViewSet(XadminViewSet):
    serializer_class = ReportListSerializer
    queryset = Report.objects.all().order_by('-pk')
    filter_class = ReportFilter
    search_fields = ["creator","updater","name","ci_job_id"]

    def get_serializer_class(self):
        if self.action == "list":
            return ReportListSerializer
        else:
            return ReportCreateUpdateSerializer

    
class ReportDetailViewSet(XadminViewSet):
    serializer_class = ReportDetailListSerializer
    queryset = ReportDetail.objects.all().order_by('-pk')
    filter_class = ReportDetailFilter
    search_fields = []

    def get_serializer_class(self):
        if self.action == "list":
            return ReportDetailListSerializer
        else:
            return ReportDetailCreateUpdateSerializer

    
class RelationViewSet(XadminViewSet):
    serializer_class = RelationListSerializer
    queryset = Relation.objects.all().order_by('-pk')
    filter_class = RelationFilter
    search_fields = []

    def get_serializer_class(self):
        if self.action == "list":
            return RelationListSerializer
        else:
            return RelationCreateUpdateSerializer

    
class VisitViewSet(XadminViewSet):
    serializer_class = VisitListSerializer
    queryset = Visit.objects.all().order_by('-pk')
    filter_class = VisitFilter
    search_fields = ["user","ip","project","url","path","request_params","request_method"]

    def get_serializer_class(self):
        if self.action == "list":
            return VisitListSerializer
        else:
            return VisitCreateUpdateSerializer

    
class UserInfoViewSet(XadminViewSet):
    serializer_class = UserInfoListSerializer
    queryset = UserInfo.objects.all().order_by('-pk')
    filter_class = UserInfoFilter
    search_fields = ["creator","updater","username","password","email"]

    def get_serializer_class(self):
        if self.action == "list":
            return UserInfoListSerializer
        else:
            return UserInfoCreateUpdateSerializer

    
class UserTokenViewSet(XadminViewSet):
    serializer_class = UserTokenListSerializer
    queryset = UserToken.objects.all().order_by('-pk')
    filter_class = UserTokenFilter
    search_fields = ["creator","updater","token"]

    def get_serializer_class(self):
        if self.action == "list":
            return UserTokenListSerializer
        else:
            return UserTokenCreateUpdateSerializer

    
class MyUserViewSet(XadminViewSet):
    serializer_class = MyUserListSerializer
    queryset = MyUser.objects.all().order_by('-pk')
    filter_class = MyUserFilter
    search_fields = ["password","username","first_name","last_name","email","phone"]

    def get_serializer_class(self):
        if self.action == "list":
            return MyUserListSerializer
        else:
            return MyUserCreateUpdateSerializer
