import json
import re
from shlex import quote

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from FasterRunner import pagination
from fastrunner import models, serializers
from fastrunner.utils import convert2hrp, response
from fastrunner.utils.convert2boomer import Boomer, BoomerExtendCmd
from fastrunner.utils.convert2hrp import Hrp
from fastrunner.utils.decorator import request_log
from fastrunner.utils.safe_json_parser import safe_json_loads


class ConvertRequest(object):
    @classmethod
    def _to_curl(cls, request, compressed=False, verify=True):
        """
        Returns string with curl command by provided request object

        Parameters
        ----------
        compressed : bool
            If `True` then `--compressed` argument will be added to result
        """
        parts = [
            ("curl", None),
            ("-X", request.method),
        ]
        parts += [
            (None, request.url),
        ]

        for k, v in sorted(request.headers.items()):
            parts += [("-H", "{0}: {1}".format(k, v))]

        if request.body:
            body = request.body
            if isinstance(body, bytes):
                body = body.decode("utf-8")
            if isinstance(body, dict):
                body = json.dumps(body)
            parts += [("-d", body)]

        if compressed:
            parts += [("--compressed", None)]

        if not verify:
            parts += [("--insecure", None)]

        flat_parts = []
        for k, v in parts:
            if k:
                flat_parts.append(quote(k))
            if v:
                flat_parts.append(quote(v))

                if k == "-H":
                    flat_parts.append(" \\\n")
        return " ".join(flat_parts)

    @classmethod
    def _make_fake_req(cls, request_meta_dict):
        class RequestMeta(object):
            ...

        req = RequestMeta()
        setattr(req, "method", request_meta_dict["method"])
        setattr(req, "url", request_meta_dict["url"])
        setattr(req, "headers", request_meta_dict["headers"])
        body = request_meta_dict.get("body") or request_meta_dict.get("data")
        setattr(req, "body", body)
        return req

    @classmethod
    def to_curl(cls, req: dict) -> str:
        _req = cls._make_fake_req(req)
        return cls._to_curl(_req, compressed=True, verify=False)

    @classmethod
    def to_hrp(cls, req: dict) -> dict:
        hrp = Hrp(faster_req_json=req)
        return hrp.get_testcase().dict()

    @classmethod
    def to_boomer(cls, req: dict) -> str:
        hrp = convert2hrp.Hrp(faster_req_json=req)
        extend_cmd = BoomerExtendCmd(replace_str_index={"$shop_id": 0})
        b = Boomer(hrp, extend_cmd)
        return b.to_boomer_cmd()

    @classmethod
    def generate_curl(cls, report_details, convert_type=("curl",)):
        for detail in report_details:
            for record in detail["records"]:
                meta_data = record["meta_data"]
                for t in convert_type:
                    req = meta_data["request"]
                    method_name = f"to_{t}"
                    method = getattr(ConvertRequest, method_name)
                    record["meta_data"][t] = method(req)


class ReportView(GenericViewSet):
    """
    报告视图
    """

    queryset = models.Report.objects
    serializer_class = serializers.ReportSerializer
    pagination_class = pagination.MyPageNumberPagination

    def get_authenticators(self):
        # 查看报告详情不需要鉴权
        # self.request.path = '/api/fastrunner/reports/3053/'
        pattern = re.compile(r"/api/fastrunner/reports/\d+/")
        if self.request.method == "GET" and re.search(pattern, self.request.path) is not None:
            return []
        return super().get_authenticators()

    @method_decorator(request_log(level="DEBUG"))
    def list(self, request):
        """报告列表"""

        project = request.query_params["project"]
        search = request.query_params["search"]
        report_type = request.query_params["reportType"]
        report_status = request.query_params["reportStatus"]
        only_me = request.query_params["onlyMe"]

        queryset = self.get_queryset().filter(project__id=project).order_by("-update_time")

        # 前端传过来是小写的字符串，不是python的True
        if only_me == "true":
            queryset = queryset.filter(creator=request.user)

        if search != "":
            queryset = queryset.filter(name__contains=search)

        if report_type != "":
            queryset = queryset.filter(type=report_type)

        if report_status != "":
            queryset = queryset.filter(status=report_status)

        page_report = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_report, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level="INFO"))
    def delete(self, request, **kwargs):
        """删除报告"""
        """
           删除一个报告pk
           删除多个
           [{
               id:int
           }]
        """
        try:
            if kwargs.get("pk"):  # 单个删除
                models.Report.objects.get(id=kwargs["pk"]).delete()
            else:
                for content in request.data:
                    models.Report.objects.get(id=content["id"]).delete()

        except ObjectDoesNotExist:
            return Response(response.REPORT_NOT_EXISTS)

        return Response(response.REPORT_DEL_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def look(self, request, **kwargs):
        """查看报告"""
        pk = kwargs["pk"]
        report = models.Report.objects.get(id=pk)
        report_detail = models.ReportDetail.objects.get(report_id=pk)
        summary = json.loads(report.summary)
        summary["details"] = safe_json_loads(report_detail.summary_detail)
        ConvertRequest.generate_curl(summary["details"], convert_type=("curl",))
        summary["html_report_name"] = report.name
        # return render_to_response('report_template.html', summary)

        return render(request, template_name="report_template.html", context=summary)

    def download(self, request, **kwargs):
        """下载报告"""
        pass
