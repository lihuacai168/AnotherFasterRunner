import json
import logging
import traceback
import types
import uuid

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from FasterRunner.customer_swagger import CustomSwaggerAutoSchema
from .models import MockAPI, MockAPILog, MockProject
from .serializers import MockAPISerializer, MockProjectSerializer

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

class RequestObject:
    def __init__(self, request):
        self.method: str = request.method
        self.headers: dict = request.headers
        self.raw_body: bytes = request.body
        # 将字节对象解码为字符串，然后使用 json.loads() 方法将其转换为字典
        decoded_data = self.raw_body.decode("utf-8")
        try:
            self.body: dict = json.loads(decoded_data)
        except Exception as e:
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
            # Generic catch-all for other errors during execution
            logger.error(
                f"Error executing the method {method_name} from module {module_name}: {e}\n {traceback.format_exc()}"
            )


def process(path, project_id, request: Request):
    try:
        logger.info(f"request path: {request.get_full_path()}")

        request_obj: dict = {
            "method": request.method.upper(),
            "path": path,
            "mock_server_full_path": request.get_full_path(),
            "body": request.data,
            "headers": request.headers._store,
            "query_params": request.query_params,
        }
        logger.debug(f"request_obj: {json.dumps(request_obj, indent=4)}")
        mock_api = MockAPI.objects.get(
            project__project_id=project_id,
            request_path=path,
            request_method=request.method.upper(),
            is_active=True,
        )
        request_id: str = uuid.uuid4().hex
        log_obj = MockAPILog.objects.create(
            request_obj=request_obj,
            request_id=request_id,
            api_id=mock_api.api_id,
            project_id=mock_api.project,
        )
        logger.debug(f"mock_api response_text\n{mock_api.response_text}")
        response = load_and_execute(
            "mock_api_module", mock_api.response_text, "execute", request
        )
        response.headers.setdefault("X-Mock-RequestId", request_id)
        response_obj = {
            "status": response.status_code,
            "body": response.data,
            "headers": response.headers._store,
        }
        logger.debug(f"response_obj: {json.dumps(response_obj, indent=4)}")
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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["project_id"] = str(uuid.uuid4().hex)
        serializer = MockProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
