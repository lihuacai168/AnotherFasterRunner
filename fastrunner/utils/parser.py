import json
import logging
from enum import Enum

logger = logging.getLogger('FasterRunner')


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

    def __init__(self, body, level='test'):
        """
        body => {
                    header: header -> [{key:'', value:'', desc:''},],
                    request: request -> {
                        form: formData - > [{key: '', value: '', type: 1, desc: ''},],
                        json: jsonData -> {},-
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

            self.__headers = body['header'].pop('header')
            self.__params = body['request']['params'].pop('params')
            self.__data = body['request']['form'].pop('data')
            self.__json = body['request'].pop('json')
            self.__files = body['request']['files'].pop('files')
            self.__variables = body['variables'].pop('variables')
            self.__setup_hooks = body['hooks'].pop('setup_hooks')
            self.__teardown_hooks = body['hooks'].pop('teardown_hooks')

            self.__desc = {
                "header": body['header'].pop('desc'),
                "data": body['request']['form'].pop('desc'),
                "files": body['request']['files'].pop('desc'),
                "params": body['request']['params'].pop('desc'),
                "variables": body['variables'].pop('desc'),
            }

            if level is 'test':
                self.url = body.pop('url')
                self.method = body.pop('method')

                self.__times = body.pop('times')
                self.__extract = body['extract'].pop('extract')
                self.__validate = body.pop('validate').pop('validate')
                self.__desc['extract'] = body['extract'].pop('desc')

            elif level is 'config':
                self.base_url = body.pop('base_url')
                self.__parameters = body['parameters'].pop('parameters')
                self.__desc["parameters"] = body['parameters'].pop('desc')

            self.__level = level
            self.testcase = None

            self.project = body.pop('project')
            self.relation = body.pop('nodeId')
            # FastRunner的API没有rig_id字段,需要兼容
            try:
                self.rig_id = body.pop('rig_id')
            except KeyError:
                self.rig_id = None

            try:
                self.rig_env = body.pop('rig_env')
            except KeyError:
                # 不传rig_env,使用默认测试环境参数0
                self.rig_id = 0
        except KeyError:
            # project or relation
            pass

    def parse(self):
        """
        返回标准化HttpRunner "desc" 字段运行需去除
        """
        try:
            if self.rig_id is not None:
                pass
        except AttributeError:
            self.rig_id = None

        try:
            if self.rig_env is not None:
                pass
        except AttributeError:
            # 不传参数,默认测试环境0
            self.rig_env = 0

        if self.__level is 'test':
            test = {
                "name": self.name,
                "rig_id": self.rig_id,
                "times": self.__times,
                "request": {
                    "url": self.url,
                    "method": self.method,
                    "verify": False
                },
                "desc": self.__desc
            }

            if self.__extract:
                test["extract"] = self.__extract
            if self.__validate:
                test['validate'] = self.__validate

        elif self.__level is 'config':
            test = {
                "name": self.name,
                "request": {
                    "base_url": self.base_url,
                },
                "desc": self.__desc
            }

            if self.__parameters:
                test['parameters'] = self.__parameters

        if self.__headers:
            test["request"]["headers"] = self.__headers
        if self.__params:
            test["request"]["params"] = self.__params
        if self.__data:
            test["request"]["data"] = self.__data
        if self.__json:
            test["request"]["json"] = self.__json
        if self.__files:
            test["request"]["files"] = self.__files
        if self.__variables:
            test["variables"] = self.__variables
        if self.__setup_hooks:
            test['setup_hooks'] = self.__setup_hooks
        if self.__teardown_hooks:
            test['teardown_hooks'] = self.__teardown_hooks

        self.testcase = test


class Parse(object):
    """
    标准HttpRunner脚本解析至前端 后端->前端
    """

    def __init__(self, body, level='test'):
        """
        body: => {
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
        self.name = body.get('name')
        self.__request = body.get('request')  # header files params json data
        self.__variables = body.get('variables')
        self.__setup_hooks = body.get('setup_hooks', [])
        self.__teardown_hooks = body.get('teardown_hooks', [])
        self.__desc = body.get('desc')

        if level is 'test':
            self.__times = body.get('times', 1)  # 如果导入没有times 默认为1
            self.__extract = body.get('extract')
            self.__validate = body.get('validate')

        elif level is "config":
            self.__parameters = body.get("parameters")

        self.__level = level
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
            content = json.dumps(content, ensure_ascii=False)
        else:
            content = str(content)
        return var_type[key], content

    def parse_http(self):
        """
        标准前端脚本格式
        """
        init = [{
            "key": "",
            "value": "",
            "desc": ""
        }]

        init_p = [{
            "key": "",
            "value": "",
            "desc": "",
            "type": 1
        }]

        #  初始化test结构
        test = {
            "name": self.name,
            "header": init,
            "request": {
                "data": init_p,
                "params": init_p,
                "json_data": ''
            },
            "variables": init_p,
            "hooks": [{
                "setup": "",
                "teardown": ""
            }]
        }

        if self.__level is 'test':
            test["times"] = self.__times
            test["method"] = self.__request['method']
            test["url"] = self.__request['url']
            test["validate"] = [{
                "expect": "",
                "actual": "",
                "comparator": "equals",
                "type": 1
            }]
            test["extract"] = init

            if self.__extract:
                test["extract"] = []
                for content in self.__extract:
                    for key, value in content.items():
                        test['extract'].append({
                            "key": key,
                            "value": value,
                            "desc": self.__desc["extract"][key]
                        })

            if self.__validate:
                test["validate"] = []
                for content in self.__validate:
                    for key, value in content.items():
                        obj = Parse.__get_type(value[1])
                        test["validate"].append({
                            "expect": obj[1],
                            "actual": value[0],
                            "comparator": key,
                            "type": obj[0]
                        })

        elif self.__level is "config":
            test["base_url"] = self.__request["base_url"]
            test["parameters"] = init

            if self.__parameters:
                test["parameters"] = []
                for content in self.__parameters:
                    for key, value in content.items():
                        test["parameters"].append({
                            "key": key,
                            "value": Parse.__get_type(value)[1],
                            "desc": self.__desc["parameters"][key]
                        })

        if self.__request.get('headers'):
            test["header"] = []
            for key, value in self.__request.pop('headers').items():
                test['header'].append({
                    "key": key,
                    "value": value,
                    "desc": self.__desc["header"][key]
                })

        if self.__request.get('data'):
            test["request"]["data"] = []
            for key, value in self.__request.pop('data').items():
                obj = Parse.__get_type(value)

                test['request']['data'].append({
                    "key": key,
                    "value": obj[1],
                    "type": obj[0],
                    "desc": self.__desc["data"][key]
                })

        # if self.__request.get('files'):
        #     for key, value in self.__request.pop("files").items():
        #         size = FileBinary.objects.get(name=value).size
        #         test['request']['data'].append({
        #             "key": key,
        #             "value": value,
        #             "size": size,
        #             "type": 5,
        #             "desc": self.__desc["files"][key]
        #         })

        if self.__request.get('params'):
            test["request"]["params"] = []
            for key, value in self.__request.pop('params').items():
                test['request']['params'].append({
                    "key": key,
                    "value": value,
                    "type": 1,
                    "desc": self.__desc["params"][key]
                })

        if self.__request.get('json'):
            test["request"]["json_data"] = \
                json.dumps(self.__request.pop("json"), indent=4,
                           separators=(',', ': '), ensure_ascii=False)
        if self.__variables:
            test["variables"] = []
            for content in self.__variables:
                for key, value in content.items():
                    obj = Parse.__get_type(value)
                    test["variables"].append({
                        "key": key,
                        "value": obj[1],
                        "desc": self.__desc["variables"][key],
                        "type": obj[0]
                    })

        if self.__setup_hooks or self.__teardown_hooks:
            test["hooks"] = []
            if len(self.__setup_hooks) > len(self.__teardown_hooks):
                for index in range(0, len(self.__setup_hooks)):
                    teardown = ""
                    if index < len(self.__teardown_hooks):
                        teardown = self.__teardown_hooks[index]
                    test["hooks"].append({
                        "setup": self.__setup_hooks[index],
                        "teardown": teardown
                    })
            else:
                for index in range(0, len(self.__teardown_hooks)):
                    setup = ""
                    if index < len(self.__setup_hooks):
                        setup = self.__setup_hooks[index]
                    test["hooks"].append({
                        "setup": setup,
                        "teardown": self.__teardown_hooks[index]
                    })
        self.testcase = test


def format_json(value):
    try:
        return json.dumps(value, indent=4, separators=(',', ': '), ensure_ascii=False)
    except:
        return value
