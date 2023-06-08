import datetime
import logging
import smtplib
import traceback

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from fastrunner.models import Visit
from fastrunner.utils import email_helper

logger = logging.getLogger(__name__)


class VisitTimesMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 复制一份body的内容，因为原生的body不能被多次访问
        request._body = request.body

    def process_response(self, request, response):

        body = request._body
        if body == b"":
            body = ""
        else:
            body = str(body, encoding="utf-8")

        url: str = request.path
        # 去除测试报告页字体相关的访问
        if '/fonts/roboto/' in url or response.headers['Content-Type'] != 'application/json':
            return response
        if request.user is None:
            # 报告页面不需要登录，获取不到用户名
            user = "AnonymousUser"
        else:
            user = request.user

        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
        # 前端请求头没传project，就默认为0
        project = request.META.get("HTTP_PROJECT", 0)

        url: str = request.path
        # 去除测试报告页字体相关的访问
        if "/fonts/roboto/" in url:
            return response

        if request.GET != {}:
            query_params = "?"
            # <QueryDict: {'page': ['1'], 'node': [''], 'project': ['11'], 'search': [''], 'tag': ['']}>
            for k, v in request.GET.items():
                query_params += f"{k}={v}&"
            if len(query_params)>200:
                query_params = ""
            url += query_params[:-1]
        else:
            query_params = ""

        Visit.objects.create(
            user=user,
            url=url,
            request_method=request.method,
            request_body=body,
            ip=ip,
            path=request.path,
            request_params=query_params[1:-1],
            project=project,
        )
        return response


class ExceptionMiddleware(MiddlewareMixin):
    @staticmethod
    def build_html_message(request, exception) -> str:
        html = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>异常</title>
</head>
<body>
    <p> 异常时间: {datetime.datetime.now()} </p>
    <p> 用户: {request.user}</p>
    <p> 请求方法: {request.method} </p>
    <p> 请求path: {request.path} </p>
    <p> 请求ID: {request.id}</p>
    <code style="background-color: #eee; border-radius: 3px; padding: 0 3px; lang: shell;"> {traceback.format_exc()}</code>
</body>
</html>
        """
        return html

    # handle exception
    def process_exception(self, request, exception):
        logger.error(traceback.format_exc())

        if (
            settings.EMAIL_HOST_USER
            and settings.EMAIL_HOST_PASSWORD
            and settings.EMAIL_HOST
            and settings.EMAIL_PORT
        ):
            try:
                email_helper.send_mail(
                    subject=f"测试平台异常告警",
                    html_message=self.build_html_message(
                        request=request, exception=exception
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                )
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f'邮件发送失败 {traceback.format_exception(e)}')
                return
            except Exception:
                logger.error(f'邮件发送失败 {traceback.format_exc()}')
                return

            logger.info("邮件发送成功")
