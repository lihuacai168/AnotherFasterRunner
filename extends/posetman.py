import json
import os
from fastrunner.utils.tree import get_tree_max_id
from fastrunner import models
import re, ast
from fastrunner.utils.parser import Format
import simplejson, uuid
from django.core.exceptions import ObjectDoesNotExist

treeId = {'node': 0}


def variables_transfer_regex(variable_str):
    flag = False
    if isinstance(variable_str, (int, float, bool)):
        return variable_str
    if isinstance(variable_str, (list, dict)):
        variable_str = str(variable_str)
        flag = True
    # transfer {{aa}} --> $aa
    pattern = re.compile(r"{{(.*?)}}")
    # transfer $-->&#36; ascii 转译 防止将$后面的内容作为变量使用
    pattern2 = re.compile(r'\$')
    variable_str = pattern2.sub('&#36;', variable_str, 0)
    matches = re.findall(pattern, variable_str)
    for match in matches:
        old = "{{" + match + "}}"
        new = "$" + match
        variable_str = variable_str.replace(old, new)
    if flag:
        # eval 有安全问题
        return ast.literal_eval(variable_str)
    return variable_str


def build_runner_script_from_postman(item, projectId):
    """
    postman item =>
    {
        'name': '文件hash创建合同',
        'event':
        [
            {
                'listen': 'prerequest',
                'script': {
                            'id': '73253ab2-442a-423e-874d-b0204a8f0622',
                            'type': 'text/javascript',
                            'exec': ['']
                }
            },
            {
                'listen': 'test',
                'script': {
                        'id': 'f6a7db48-a18d-4726-8769-585fbcbd4b15',
                        'type': 'text/javascript',
                        'exec': ['']
                }
            }
        ],
        'request': {
            'method': 'POST',
            'header': [
                        {'key': 'Content-Type', 'value': 'application/json'},
                        {'key': 'X-Tsign-Open-App-Id', 'value': '{{project_id}}'},
                        {'key': 'X-Tsign-Open-App-Secret', 'value': '{{xuemeng_secrect}}'}
                      ],
            'body': {
                        'mode': 'raw',
                        'raw': '{\r\n    "fileHash": "34657864dfgfh",\r\n    "fileKey":"bjsbhd678938",\r\n    "name":"非hash文件"\r\n}'
                    },
            'url': {
                'raw': '{{openapi}}/doc/createbyfilehash',
                'host': ['{{openapi}}'],
                'path': ['doc', 'createbyfilehash']
            }
        },
        'response': []
    }
    ------------------------------------------------------------------------------------------------

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
    body = {
        'name': variables_transfer_regex(item.get('name')),
        'request': {
            'form': {
                'data': {},
                'desc': {}
            },
            'json': {},
            'params': {
                'params': {},
                'desc': {}
            },
            'files': {
                'files': {},
                'desc': {}
            }
        },
        'extract': {
            'extract': [],
            'desc': {}
        },
        'validate': {
            'validate': []
        },
        'variables': {
            'variables': [],
            'desc': {}
        },
        'hooks': {
            'setup_hooks': [],
            'teardown_hooks': []
        },
        'times': 1,
        "project": projectId
    }
    if item.get('request'):
        request = item.get('request')
        body['method'] = request.get('method')
        body['url'] = variables_transfer_regex(request['url']['raw'])
        body['nodeId'] = treeId['node']
        headers = {}
        headers_desc = {}
        for item in request['header']:
            headers[item.get('key')] = variables_transfer_regex(item.get('value'))
            headers_desc[item.get('key')] = item.get('description', '')

        body['header'] = {
            'header': headers,
            'desc': headers_desc
        }
        mode = request['body']['mode']
        if mode == "urlencoded":
            urlencoded_dict = {}
            urlencodedsDict_desc = {}
            urlencodeds = request['body']['urlencoded']
            for item in urlencodeds:
                urlencoded_dict[item.get('key')] = variables_transfer_regex(item.get('value'))
                urlencodedsDict_desc[item.get('key')] = item.get('description', '')
            body['request']['params']['params'] = urlencoded_dict
            body['request']['params']['desc'] = urlencodedsDict_desc
        if mode == "formdata":
            form_data_dict = {}
            form_data_desc = {}
            form_datas = request['body']['formdata']
            for item in form_datas:
                form_data_dict[item.get('key')] = variables_transfer_regex(item.get('value'))
                form_data_desc[item.get('key')] = item.get('description', '')
            body['request']['form']['data'] = form_data_dict
            body['request']['form']['desc'] = form_data_desc
        if mode == "raw":
            strs = variables_transfer_regex(request['body']['raw'])
            if strs != "":
                body['request']['json'] = simplejson.loads(strs)
        if mode == "file":
            body['request']['files']['files'] = request['body']['file']
    api = Format(body)
    api.parse()
    api_body = {
        'name': api.name,
        'body': api.testcase,
        'url': api.url,
        'method': api.method,
        'project': models.Project.objects.get(id=api.project),
        'relation': api.relation
    }
    models.API.objects.create(**api_body)


def recursive_collection_item(items, folder, project_id):
    if not isinstance(items, list):
        raise TypeError("collection item must be a list")
    for item in items:
        if not item.get('item'):
            build_runner_script_from_postman(item, project_id)
        else:
            nodeId = treeId['node'] + 1
            treeId['node'] = nodeId
            node = {
                "id": treeId['node'],
                "label": item.get('name'),
                "children": []
            }
            recursive_collection_item(item['item'], node, project_id)
            folder['children'].append(node)
    return folder


# transfer is related by postman 2.1.0 colletion Schemas
# which is from https://schema.getpostman.com/json/collection/v2.1.0/collection.json
def transfer_postman_cases_to_http_runner_cases(content, projectId):
    """
    :param content: type dict or json only show required fields
        {
            "info":{
                "name": test,
                "schema": https://schema.getpostman.com/json/collection/v2.1.0/collection.json
            }
            "item":[{
                "name": "case_1",
                "request":{
                },{
                "name": "测试",
                "item":[{
                    "name": "case_2",
                    "request":{
                    }
                }]
                }
            }]
        }
    :return:
    """
    tree = models.Relation.objects.get(project__id=projectId, type=1)
    body = eval(tree.tree)
    treeId['node'] = get_tree_max_id(body) + 1
    parent = {
        "id": treeId['node'],
        "label": content['info']['name'],
        "children": []
    }
    folder = recursive_collection_item(content['item'], parent, projectId)
    body.append(folder)
    tree.tree = str(body)
    tree.save()
    treeId['node'] = 0


def transfer_postman_environment_to_config(content, project):
    config = {
        'parameters': {
            'parameters': [],
            'desc': {}
        },
        'header':
            {'header': {},
             'desc': {}
             },
        'request': {
            'form': {
                'data': {},
                'desc': {}
            },
            'json': {},
            'params':
                {
                    'params': {},
                    'desc': {}
                },
            'files': {
                'files': {},
                'desc': {}
            }
        },
        'variables': {
            'variables': [],
            'desc': {}
        },
        'hooks': {
            'setup_hooks': [],
            'teardown_hooks': []
        },
        'base_url': 'postman转换数据,请修改',
        'name': str(uuid.uuid4()),
        'project': project
    }
    if content.get('values'):
        for item in content.get('values'):
            value = item.get('value')
            if value is None or value == '':
                value = ''
            tmp = {item.get('key'): variables_transfer_regex(value)}
            config['variables']['variables'].append(tmp)
            if item.get('description'):
                value1 = item['description'].get('content')
                if value1 is None or value1 == '':
                    value1 = ''
                config['variables']['desc'][item.get('key')] = value1
            else:
                config['variables']['desc'][item.get('key')] = ''
    config = Format(config, level='config')
    config.parse()

    try:
        config.project = models.Project.objects.get(id=project)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("项目不存在，请重试")
    config_body = {
        "name": config.name,
        "base_url": config.base_url,
        "body": config.testcase,
        "project": config.project
    }
    models.Config.objects.create(**config_body)


def test_config():
    collection_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "tmp",
        "开放服务_测试环境.postman_environment.json"
    )
    with open(collection_path, encoding='utf-8') as collection:
        json_con = json.load(collection)
        transfer_postman_environment_to_config(json_con, 1)


def test():
    collection_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "tmp",
        "开放服务-VPC.postman_collection.json"
    )
    with open(collection_path, encoding='utf-8') as collection:
        json_con = json.load(collection)
        transfer_postman_cases_to_http_runner_cases(json_con, 1)
