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
    解析标准HttpRunner脚本
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

            self.relation = body.pop('nodeId')
            self.project = body.pop('project')

            self.desc = {
                "header": body['header'].pop('desc'),
                "data": body['request']['form'].pop('desc'),
                "files": body['request']['files'].pop('desc'),
                "params": body['request']['params'].pop('desc'),
                "extract": body['extract'].pop('desc'),
                "variables": body['variables'].pop('desc'),
            }

            self.testcase=None
        except KeyError:
            self.msg = 'url or method or name is missed'

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