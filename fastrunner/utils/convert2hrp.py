import json
import os
from collections.abc import Callable
from enum import Enum
from typing import Any, Dict, List, Text, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, HttpUrl

Name = str
Url = str
BaseUrl = Union[HttpUrl, str]
VariablesMapping = dict[str, Any]
FunctionsMapping = dict[str, Callable]
Headers = dict[str, str]
Cookies = dict[str, str]
Verify = bool
Hooks = list[str | dict[str, str]]
Export = list[str]
Validators = list[dict]
Env = dict[str, Any]


class MethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    NA = "N/A"


class TConfig(BaseModel):
    name: Name
    verify: Verify = False
    base_url: BaseUrl = ""
    # Text: prepare variables in debugtalk.py, ${gen_variables()}
    variables: VariablesMapping | str = {}
    parameters: VariablesMapping | str = {}
    # setup_hooks: Hooks = []
    # teardown_hooks: Hooks = []
    export: Export = []
    path: str = None
    weight: int = 1


class TRequest(BaseModel):
    """requests.Request model"""

    method: MethodEnum
    url: Url
    params: dict[str, str] = {}
    headers: Headers = {}
    req_json: dict | list | str = Field(None)
    body: str | dict[str, Any] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: dict = {}  # used for upload files


class TStep(BaseModel):
    name: Name
    request: TRequest | None = None
    testcase: str | Callable | None = None
    variables: VariablesMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    # used to extract request's response field
    extract: VariablesMapping = {}
    # used to export session variables from referenced testcase
    export: Export = []
    validators: Validators = Field([], alias="validate")
    validate_script: list[str] = []


class TestCase(BaseModel):
    config: TConfig
    teststeps: list[TStep]


class ProjectMeta(BaseModel):
    debugtalk_py: str = ""  # debugtalk.py file content
    debugtalk_path: str = ""  # debugtalk.py file path
    dot_env_path: str = ""  # .env file path
    functions: FunctionsMapping = {}  # functions defined in debugtalk.py
    env: Env = {}
    RootDir: str = os.getcwd()  # project root directory (ensure absolute), the path debugtalk.py located


class TestsMapping(BaseModel):
    project_meta: ProjectMeta
    testcases: list[TestCase]


class TestCaseTime(BaseModel):
    start_at: float = 0
    start_at_iso_format: str = ""
    duration: float = 0


class TestCaseInOut(BaseModel):
    config_vars: VariablesMapping = {}
    export_vars: dict = {}


class RequestStat(BaseModel):
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    client_ip: str = "N/A"
    client_port: int = 0
    server_ip: str = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    method: MethodEnum = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: str | bytes | list | dict | None = {}


class ResponseData(BaseModel):
    status_code: int
    headers: dict
    cookies: Cookies
    encoding: str | None = None
    content_type: str
    body: str | bytes | list | dict


class ReqRespData(BaseModel):
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """request session data, including request, response, validators and stat data"""

    success: bool = False
    # in most cases, req_resps only contains one request & response
    # while when 30X redirect occurs, req_resps will contain multiple request & response
    req_resps: list[ReqRespData] = []
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: dict = {}


class StepData(BaseModel):
    """teststep data, each step maybe corresponding to one request or one testcase"""

    success: bool = False
    name: str = ""  # teststep name
    data: SessionData | list["StepData"] = None
    export_vars: VariablesMapping = {}


StepData.update_forward_refs()


class TestCaseSummary(BaseModel):
    name: str
    success: bool
    case_id: str
    time: TestCaseTime
    in_out: TestCaseInOut = {}
    log: str = ""
    step_datas: list[StepData] = []


class PlatformInfo(BaseModel):
    httprunner_version: str
    python_version: str
    platform: str


class TestCaseRef(BaseModel):
    name: str
    base_url: str = ""
    testcase: str
    variables: VariablesMapping = {}


class TestSuite(BaseModel):
    config: TConfig
    testcases: list[TestCaseRef]


class Stat(BaseModel):
    total: int = 0
    success: int = 0
    fail: int = 0


class TestSuiteSummary(BaseModel):
    success: bool = False
    stat: Stat = Stat()
    time: TestCaseTime = TestCaseTime()
    platform: PlatformInfo
    testcases: list[TestCaseSummary]


class Hrp:
    def __init__(self, faster_req_json: dict):
        self.faster_req_json = faster_req_json

    def parse_url(self):
        url = self.faster_req_json["url"]
        o = urlparse(url=url)
        baseurl = o.scheme + "://" + o.netloc
        return baseurl, o.path

    def get_headers(self):
        headers: dict = self.faster_req_json.get("headers", {})
        # Content-Length may be error
        headers.pop("Content-Length", None)
        return headers

    def get_request(self) -> TRequest:
        base_url, path = self.parse_url()
        req = TRequest(
            method=self.faster_req_json["method"],
            url=base_url + path,
            params=self.faster_req_json.get("params", {}),
            headers=self.get_headers(),
            body=self.faster_req_json.get("body", {}),
            req_json=self.faster_req_json.get("json", {}),
            verify=self.faster_req_json.get("verify", False),
        )
        return req

    def get_step(self) -> TStep:
        _, path = self.parse_url()
        return TStep(
            name=path,
            request=self.get_request(),
        )

    def get_config(self) -> TConfig:
        base_url, _ = self.parse_url()
        return TConfig(
            name=base_url,
            base_url=base_url,
        )

    def get_testcase(self) -> TestCase:
        config = self.get_config()
        teststeps: list = [self.get_step()]
        return TestCase(
            config=config,
            teststeps=teststeps,
        )


source_json = """
{
  "url": "http://10.129.144.22:8081/post",
  "method": "POST",
  "headers": {
    "User-Agent": "python-requests/2.22.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=utf-8",
    "userId": "0123456",
    "Content-Length": "251"
  },
  "setup_hooks_start": 1647079497.715158,
  "setup_hooks_duration": 0,
  "json": {
    "firstName": "John",
    "lastName": "doe",
    "age": 26,
    "address": {
      "streetAddress": "naist street",
      "city": "Nara",
      "postalCode": "630-0192"
    },
    "phoneNumbers": [
      {
        "type": "iPhone",
        "number": "0123-4567-8888"
      },
      {
        "type": "home",
        "number": "0123-4567-8910"
      }
    ]
  },
  "verify": false,
  "body": {
    "firstName": "John",
    "lastName": "doe",
    "age": 26,
    "address": {
      "streetAddress": "naist street",
      "city": "Nara",
      "postalCode": "630-0192"
    },
    "phoneNumbers": [
      {
        "type": "iPhone",
        "number": "0123-4567-8888"
      },
      {
        "type": "home",
        "number": "0123-4567-8910"
      }
    ]
  }
}
"""

if __name__ == "__main__":
    hrp = Hrp(json.loads(source_json))
    print(hrp.get_testcase().json())
