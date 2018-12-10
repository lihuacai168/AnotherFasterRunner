from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from FasterRunner import pagination
from fastrunner import models, serializers


class ReportView(GenericViewSet):
    """
    报告视图
    """
    authentication_classes = ()
    queryset = models.Report.objects.all().order_by('-update_time')
    serializer_class = serializers.ReportSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request):
        """报告列表
        """

        report = self.get_queryset()
        page_report = self.paginate_queryset(report)
        serializer = self.get_serializer(page_report, many=True)
        return self.get_paginated_response(serializer.data)

    def delete(self, request):
        """删除报告
        """
        pass

    def look(self, request, **kwargs):
        """查看报告
        """
        pk = kwargs["pk"]
        summary = models.Report.objects.get(id=pk).summary
        return Response(summary)

    def download(self, request, **kwargs):
        """下载报告
        """
        pass
