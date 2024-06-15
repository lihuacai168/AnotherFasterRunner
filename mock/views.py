import json
import logging
import traceback
import types
import uuid
from datetime import datetime


from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from FasterRunner.customer_swagger import CustomSwaggerAutoSchema
from .models import MockAPI, MockAPILog, MockProject
from .serializers import MockAPISerializer, MockProjectSerializer, MockAPILogSerializer

logger = logging.getLogger(__name__)


# mock function demo
def execute(req, resp):
    import requests

    url = "http://localhost:8000/api/mock/mock_api/"

    payload = {}
    headers = {
        "accept": "application/json",
        "X-CSRFToken": "fk5wQDlKC6ufRjk7r38pfbqyq7mTtyc5NUUqkFN5lbZf6nyHVSbAUVoqbwaGcQHT",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp.data = response.json()


class MockAPIFilter(filters.FilterSet):
    project_name = filters.CharFilter(field_name='project__project_name', lookup_expr='icontains')
    api_name = filters.CharFilter(lookup_expr="icontains")
    request_path = filters.CharFilter(lookup_expr="icontains")
    creator = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = MockAPI
        fields = ["project__project_name", "api_name", "creator", "request_path"]


class MockAPIViewset(viewsets.ModelViewSet):
    swagger_tag = '项目下的Mock API CRUD'
    swagger_schema = CustomSwaggerAutoSchema
    queryset = MockAPI.objects.all()
    serializer_class = MockAPISerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MockAPIFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 获取传入的版本号
        incoming_version = request.data.get('version')

        # 如果数据库中的版本号比传入的版本号更大，阻止更新并返回错误
        if incoming_version is not None and instance.version > int(incoming_version):
            return Response({
                'status': 'error',
                'message': 'There is a newer version of this API already saved.'
            }, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 序列化器保存了实例，但我们还没有更新版本号
        self.perform_update(serializer)

        # 保存成功后，递增版本号并更新实例
        instance.version += 1
        instance.save(update_fields=['version'])  # 只更新版本字段

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RequestObject:
    def __init__(self, request):
        self.method: str = request.method
        self.headers: dict = request.headers
        self.raw_body: bytes = request.body
        # body是json类型时
        if request.content_type == "application/json":
            # 将字节对象解码为字符串，然后使用 json.loads() 方法将其转换为字典
            decoded_data = self.raw_body.decode("utf-8")
            try:
                self.body: dict = json.loads(decoded_data)
            except Exception as e:
                self.body = {}
        elif request.content_type == "application/x-www-form-urlencoded":
            # body是表单类型时
            self.body: dict = request.data
        else:
            self.body = {}
        self.query_params: dict = request.query_params
        self.path: str = request._request.path
        # Add any other properties you would like to ease access to


def dynamic_load_module(module_name, code):
    # Create a new module with the given name
    module = types.ModuleType(module_name)
    try:
        # Execute the code in the module's context
        exec(code, module.__dict__)
        # Return the created module
        return module
    except SyntaxError as e:
        logger.error(f"SyntaxError during loading module {module_name}: {e}")


def load_and_execute(module_name, code, method_name, request) -> Response:
    module = dynamic_load_module(module_name, code)
    if module is not None:
        try:
            # Check if the method exists in the module
            if hasattr(module, method_name):
                # If the method exists, get it
                method = getattr(module, method_name)
                # Prepare a request object
                req_obj: RequestObject = RequestObject(request)
                # Execute method with request_object as an argument

                resp_obj = Response()
                method(req_obj, resp_obj)
                return resp_obj
            else:
                # If the method does not exist, log an error
                logger.error(
                    f"The method {method_name} does not exist in the module {module_name}"
                )
                data = {"error": f"Module should has {method_name} method"}
                return Response(data=data)
        except Exception as e:
            raise e


def convert_to_kv(input_dict):
    """
    将包含元组值的字典转换为键值对字典。

    参数:
    input_dict (dict): 输入字典，其中值为包含两个元素的元组。

    返回:
    dict: 简单的键值对字典。
    """
    return {value[0]: value[1] for key, value in input_dict.items()}


def process(path, project_id, request: Request):
    try:
        req_time = datetime.now()
        if settings.IS_PERF == '0':
            logger.info(f"request path: {request.get_full_path()}")

        request_obj: dict = {
            "method": request.method.upper(),
            "path": path,
            "mock_server_full_path": request.get_full_path(),
            "body": request.data,
            "headers": convert_to_kv(request.headers._store),
            "query_params": request.query_params,
        }
        if settings.IS_PERF == '0':
            logger.info(f"request_obj: {json.dumps(request_obj, indent=4)}")

        mock_api = MockAPI.objects.get(
            project__project_id=project_id,
            request_path=path,
            request_method=request.method.upper(),
            is_active=True,
        )
        request_id: str = uuid.uuid4().hex

        response = load_and_execute(
            "mock_api_module", mock_api.response_text, "execute", request
        )
        response.headers.setdefault("X-Mock-RequestId", request_id)
        response_obj = {
            "status": response.status_code,
            "body": response.data,
            "headers": convert_to_kv(response.headers._store),
        }
        if settings.IS_PERF == '0':
            logger.info(f"response_obj: {json.dumps(response_obj, indent=4)}")
            log_obj = MockAPILog.objects.create(
                request_obj=request_obj,
                request_id=request_id,
                api_id=mock_api.api_id,
                project_id=mock_api.project,
                create_time=req_time
            )
            log_obj.response_obj = response_obj
            log_obj.save()
        if response is not None:
            return response
        return Response({"error": "Execution failure"})
    except MockAPI.DoesNotExist:
        logger.error(
            f"Mock API does not exist for project_id: {project_id}, path: {path}, method: {request.method}"
        )
        return Response({"error": "Mock API does not exist"})
    except Exception as e:
        logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
        return Response(
            {"error": f"An unexpected error occurred, {traceback.format_exc()}"}
        )


class MockAPIView(APIView):
    authentication_classes = []

    @swagger_auto_schema(tags=["外部调用的mockapi"])
    def get(self, request: Request, project_id: str, path: str) -> Response:
        return self.process_request(path, project_id, request)

    @swagger_auto_schema(tags=["外部调用的mockapi"])
    def post(self, request: Request, project_id: str, path: str) -> Response:
        return self.process_request(path, project_id, request)

    @swagger_auto_schema(tags=["外部调用的mockapi"])
    def put(self, request: Request, project_id: str, path: str) -> Response:
        return self.process_request(path, project_id, request)

    @swagger_auto_schema(tags=["外部调用的mockapi"])
    def delete(self, request: Request, project_id: str, path: str) -> Response:
        return self.process_request(path, project_id, request)

    def process_request(self, path: str, project_id: str, request: Request) -> Response:
        return process(path, project_id, request)


class MockProjectFilter(filters.FilterSet):
    project_name = filters.CharFilter(lookup_expr="icontains")
    project_desc = filters.CharFilter(lookup_expr="icontains")
    creator = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = MockProject
        fields = ["project_name", "project_desc", "creator"]


class MockProjectViewSet(viewsets.ModelViewSet):
    swagger_tag = 'Mock Project CRUD'
    swagger_schema = CustomSwaggerAutoSchema
    queryset = MockProject.objects.all()
    serializer_class = MockProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MockProjectFilter


class MockAPILogFilter(filters.FilterSet):
    request_id = filters.CharFilter(lookup_expr="icontains")
    request_path = filters.CharFilter(method="filter_by_request_path")

    class Meta:
        model = MockAPILog
        fields = ["request_id", "request_path"]

    def filter_by_request_path(self, queryset, name, value):
        return queryset.filter(api__request_path__icontains=value)


class MockAPILogViewSet(viewsets.ModelViewSet):
    swagger_tag = 'Mock API Log CRUD'
    swagger_schema = CustomSwaggerAutoSchema
    queryset = MockAPILog.objects.select_related('api', 'project').all()
    serializer_class = MockAPILogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MockAPILogFilter
    search_fields = ['request_id', 'api__request_path']
