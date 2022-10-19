from tyadmin_api import auto_views
from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter(trailing_slash=False)
    
router.register('permission', auto_views.PermissionViewSet)
    
router.register('group', auto_views.GroupViewSet)
    
router.register('content_type', auto_views.ContentTypeViewSet)
    
router.register('project', auto_views.ProjectViewSet)
    
router.register('debugtalk', auto_views.DebugtalkViewSet)
    
router.register('config', auto_views.ConfigViewSet)
    
router.register('a_p_i', auto_views.APIViewSet)
    
router.register('case', auto_views.CaseViewSet)
    
router.register('case_step', auto_views.CaseStepViewSet)
    
router.register('host_i_p', auto_views.HostIPViewSet)
    
router.register('variables', auto_views.VariablesViewSet)
    
router.register('report', auto_views.ReportViewSet)
    
router.register('report_detail', auto_views.ReportDetailViewSet)
    
router.register('relation', auto_views.RelationViewSet)
    
router.register('visit', auto_views.VisitViewSet)
    
router.register('user_info', auto_views.UserInfoViewSet)
    
router.register('user_token', auto_views.UserTokenViewSet)
    
router.register('my_user', auto_views.MyUserViewSet)
    
urlpatterns = [
        re_path('^', include(router.urls)),
    ]
    