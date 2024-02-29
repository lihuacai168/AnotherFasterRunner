import json
import logging
import traceback
import types
import uuid

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MockAPI, MockProject
from .serializers import MockAPISerializer, MockProjectSerializer

logger = logging.getLogger(__name__)


def execute():
    import requests

    url = "http://localhost:8000/api/mock/mock_api/"

    payload = {}
    headers = {
        "accept": "application/json",
        "X-CSRFToken": "fk5wQDlKC6ufRjk7r38pfbqyq7mTtyc5NUUqkFN5lbZf6nyHVSbAUVoqbwaGcQHT",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


class MockAPIViewset(viewsets.ModelViewSet):
    queryset = MockAPI.objects.all()
    serializer_class = MockAPISerializer
    authentication_classes = []


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


def load_and_execute(module_name, code, method_name, request):
    module = dynamic_load_module(module_name, code)
    if module is not None:
        try:
            # Check if the method exists in the module
            if hasattr(module, method_name):
                # If the method exists, get it
                method = getattr(module, method_name)
                # Prepare a request object
                request_object = RequestObject(request)
                # Execute method with request_object as an argument
                return method(request_object)
            else:
                # If the method does not exist, log an error
                logger.error(f"The method {method_name} does not exist in the module {module_name}")
                return {"error": f"Module should has {method_name} method"}
        except Exception as e:
            # Generic catch-all for other errors during execution
            logger.error(
                f"Error executing the method {method_name} from module {module_name}: {e}\n {traceback.format_exc()}"
            )


def process(path, project_id, request):
    try:
        logger.info(f"project_id: {project_id}, path: {path}")
        mock_api = MockAPI.objects.get(
            project__project_id=project_id, request_path=path, request_method=request.method.upper(), is_active=True
        )
        logger.info(f"mock_api obj\n{mock_api.response_text}")
        response = load_and_execute("mock_api_module", mock_api.response_text, "execute", request)
        if response is not None:
            return Response(response)
        return Response({"error": "Execution failure"})
    except MockAPI.DoesNotExist:
        logger.error(f"Mock API does not exist for project_id: {project_id}, path: {path}, method: {request.method}")
        return Response({"error": "Mock API does not exist"})
    except Exception as e:
        logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
        return Response({"error": f"An unexpected error occurred, {traceback.format_exc()}"})


class MockAPIView(APIView):
    authentication_classes = []

    def get(self, request, project_id, path):
        return process(path, project_id, request)

    def post(self, request, project_id, path):
        return process(path, project_id, request)

    def put(self, request, project_id, path):
        return process(path, project_id, request)

    def delete(self, request, project_id, path):
        return process(path, project_id, request)

    def patch(self, request, project_id, path):
        return process(path, project_id, request)


class MockProjectViewSet(viewsets.ModelViewSet):
    queryset = MockProject.objects.all()
    serializer_class = MockProjectSerializer
    authentication_classes = []

    def create(self, request):
        data = request.data.copy()
        data["project_id"] = str(uuid.uuid4().hex)
        serializer = MockProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
