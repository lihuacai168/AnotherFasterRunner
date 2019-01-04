import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from FasterRunner import pagination
from fastrunner import models, serializers
from fastrunner.utils import response


class ReportView(GenericViewSet):
    """
    报告视图
    """
    authentication_classes = ()
    queryset = models.Report.objects
    serializer_class = serializers.ReportSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request):
        """报告列表
        """

        report = self.get_queryset().filter(project__id=request.query_params["project"]).order_by('-update_time')
        page_report = self.paginate_queryset(report)
        serializer = self.get_serializer(page_report, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request, **kwargs):
        """删除报告
        """
        """
               删除一个报告pk
               删除多个
               [{
                   id:int
               }]
               """
        try:
            if kwargs.get('pk'):  # 单个删除
                models.Report.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.Report.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.REPORT_NOT_EXISTS)

        return Response(response.REPORT_DEL_SUCCESS)

    def look(self, request, **kwargs):
        """查看报告
        """
        pk = kwargs["pk"]
        report = models.Report.objects.get(id=pk)
        summary = json.loads(report.summary, encoding="utf-8")
        summary["html_report_name"] = report.name
        return render_to_response('report_template.html', summary)

    def download(self, request, **kwargs):
        """下载报告
        """
        pass
