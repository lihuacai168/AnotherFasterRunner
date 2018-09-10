import json
from enum import Enum


class FileType(Enum):
    """
    文件类型枚举
    """
    string = 1
    int = 2
    float = 3
    bool = 4
    list = 5
    dict = 6
    file = 7


class Format(object):
    """
    解析标准HttpRunner脚本 前端->后端
    """

    def __init__(self, body):
        """
        body => {
                    header: header -> [{key:'', value:'', desc:''},],
                    request: request -> {
                        form: formData - > [{key: '', value: '', type: 1, desc: ''},],
                        json: jsonData -> {},
                        params: paramsData -> [{key: '', value: '', type: 1, desc: ''},]
                        files: files -> {"fields","binary"}
                    },
                    extract: extract -> [{key:'', value:'', desc:''}],
                    validate: validate -> [{expect: '', actual: '', comparator: 'equals', type: 1},],
                    variables: variables -> [{key: '', value: '', type: 1, desc: ''},],
                    hooks: hooks -> [{setup: '', teardown: ''},],
                    url: url -> string
                    method: method -> string
                    name: name -> string
                }
        """

        try:
            self.name = body.pop('name')
            self.url = body.pop('url')
            self.method = body.pop('method')
            self.times = body.pop('times')

            self.headers = body['header'].pop('header')
            self.params = body['request']['params'].pop('params')
            self.data = body['request']['form'].pop('data')
            self.json = body['request'].pop('json')
            self.files = body['request']['files'].pop('files')

            self.variables = body['variables'].pop('variables')
            self.extract = body['extract'].pop('extract')
            self.validate = body.pop('validate').pop('validate')
            self.setup_hooks = body['hooks'].pop('setup_hooks')
            self.teardown_hooks = body['hooks'].pop('teardown_hooks')

            self.desc = {
                "header": body['header'].pop('desc'),
                "data": body['request']['form'].pop('desc'),
                "files": body['request']['files'].pop('desc'),
                "params": body['request']['params'].pop('desc'),
                "extract": body['extract'].pop('desc'),
                "variables": body['variables'].pop('desc'),
            }

            self.relation = body.pop('nodeId')
            self.project = body.pop('project')

            self.testcase = None
        except KeyError:
            pass

    def parse_test(self):
        """
        返回标准化HttpRunner "desc" 字段运行需去除
        """
        test = {
            "name": self.name,
            "times": self.times,
            "request": {
                "url": self.url,
                "method": self.method
            },
            "desc": self.desc
        }

        if self.headers:
            test["request"]["headers"] = self.headers
        if self.params:
            test["request"]["params"] = self.params
        if self.data:
            test["request"]["data"] = self.data
        if self.json:
            test["request"]["json"] = self.json
        if self.files:
            test["request"]["files"] = self.files

        if self.extract:
            test["extract"] = self.extract
        if self.validate:
            test['validate'] = self.validate
        if self.variables:
            test["variables"] = self.variables
        if self.setup_hooks:
            test['setup_hooks'] = self.setup_hooks
        if self.teardown_hooks:
            test['teardown_hooks'] = self.teardown_hooks

        self.testcase = test


class Parse(object):
    """
    标准HttpRunner脚本解析至前端 后端->前端
    """

    def __init__(self, body):
        """
        body: =>{
                "name": "get token with $user_agent, $os_platform, $app_version",
                "request": {
                    "url": "/api/get-token",
                    "method": "POST",
                    "headers": {
                        "app_version": "$app_version",
                        "os_platform": "$os_platform",
                        "user_agent": "$user_agent"
                    },
                    "json": {
                        "sign": "${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
                    },
                    "extract": [
                        {"token": "content.token"}
                    ],
                    "validate": [
                        {"eq": ["status_code", 200]},
                        {"eq": ["headers.Content-Type", "application/json"]},
                        {"eq": ["content.success", true]}
                    ],
                    "setup_hooks": [],
                    "teardown_hooks": []
                }
        """
        self.name = body.get('name', '')
        self.times = body.get('times', 1)  # 如果导入没有times 默认为1
        self.request = body.get('request')  # header files params json data
        self.variables = body.get('variables')
        self.extract = body.get('extract')
        self.validate = body.get('validate')
        self.setup_hooks = body.get('setup_hooks', [])
        self.teardown_hooks = body.get('teardown_hooks', [])
        self.desc = body.get('desc')

        self.testcase = None

    @staticmethod
    def __get_type(content):
        """
        返回data_type 默认string
        """
        var_type = {
            "str": 1,
            "int": 2,
            "float": 3,
            "bool": 4,
            "list": 5,
            "dict": 6,
        }

        key = str(type(content).__name__)

        if key in ["list", "dict"]:
            content = json.dumps(content)
        else:
            content = str(content)
        return var_type[key], content

    def parse_http(self):
        """
        标准前端脚本格式
        """
        init = {
            "key": "",
            "value": "",
            "desc": ""
        }

        init_p = {
            "key": "",
            "value": "",
            "desc": "",
            "type": 1
        }

        #  初始化test结构
        test = {
            "name": self.name,
            "times": self.times,
            "url": self.request['url'],
            "method": self.request['method'],
            "header": [init],
            "request": {
                "data": [init_p],
                "params": [init_p],
                "json_data": ''
            },
            "validate": [{
                "expect": "",
                "actual": "",
                "comparator": "equals",
                "type": 1
            }],
            "variables": [init_p],
            "extract": [init],
            "hooks": [{
                "setup": "",
                "teardown": ""
            }]
        }

        if self.request.get('headers'):
            test["header"] = []
            for key, value in self.request.pop('headers').items():
                test['header'].append({
                    "key": key,
                    "value": value,
                    "desc": self.desc["header"][key]
                })

        if self.request.get('data'):
            test["request"]["data"] = []
            for key, value in self.request.pop('data').items():
                obj = Parse.__get_type(value)

                test['request']['data'].append({
                    "key": key,
                    "value": obj[1],
                    "type": obj[0],
                    "desc": self.desc["data"][key]
                })

        if self.request.get('params'):
            test["request"]["params"] = []
            for key, value in self.request.pop('params').items():
                test['request']['params'].append({
                    "key": key,
                    "value": value,
                    "type": 1,
                    "desc": self.desc["params"][key]
                })

        if self.request.get('json'):
            test["request"]["json_data"] = \
                json.dumps(self.request.pop("json"), indent=4,
                           separators=(',', ': '), ensure_ascii=False)

        if self.extract:
            test["extract"] = []
            for content in self.extract:
                for key, value in content.items():
                    test['extract'].append({
                        "key": key,
                        "value": value,
                        "desc": self.desc["extract"][key]
                    })

        if self.variables:
            test["variables"] = []
            for content in self.variables:
                for key, value in content.items():
                    obj = Parse.__get_type(value)
                    test["variables"].append({
                        "key": key,
                        "value": obj[1],
                        "desc": self.desc["variables"][key],
                        "type": obj[0]
                    })

        if self.validate:
            test["validate"] = []
            for content in self.validate:
                for key, value in content.items():
                    obj = Parse.__get_type(value[1])
                    test["validate"].append({
                        "expect": obj[1],
                        "actual": value[0],
                        "comparator": key,
                        "type": obj[0]
                    })

        if self.setup_hooks or self.teardown_hooks:
            test["hooks"] = []
            if len(self.setup_hooks) > len(self.teardown_hooks):
                for index in range(0, len(self.setup_hooks)):
                    teardown = ""
                    if index < len(self.teardown_hooks):
                        teardown = self.teardown_hooks[index]
                    test["hooks"].append({
                        "setup": self.setup_hooks[index],
                        "teardown": teardown
                    })
            else:
                for index in range(0, len(self.teardown_hooks)):
                    setup = ""
                    if index < len(self.setup_hooks):
                        setup = self.setup_hooks[index]
                    test["hooks"].append({
                        "setup": setup,
                        "teardown": self.teardown_hooks[index]
                    })

        self.testcase = test
