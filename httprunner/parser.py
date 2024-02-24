import ast
import logging
import re

# from loguru import logger
from httprunner import exceptions, utils
from httprunner.compat import basestring, builtin_str, numeric_types, str

variable_regexp = r"\$([\w_]+)"
function_regexp = r"\$\{([\w_]+\([\$\w\.\-/_ =,]*\))\}"
function_regexp_compile = re.compile(r"^([\w_]+)\(([\$\w\.\-/_ =,]*)\)$")

# use $$ to escape $ notation
dolloar_regex_compile = re.compile(r"\$\$")
# variable notation, e.g. ${var} or $var
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# function notation, e.g. ${func1($var_1, $var_3)}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")


logger = logging.getLogger("httprunner")


def parse_string_value(str_value):
    """parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def extract_variables(content):
    """extract all variable names from content, which is in format $variable

    Args:
        content (str): string content

    Returns:
        list: variables list extracted from string content

    Examples:
        >>> extract_variables("$variable")
        ["variable"]

        >>> extract_variables("/blog/$postid")
        ["postid"]

        >>> extract_variables("/$var1/$var2")
        ["var1", "var2"]

        >>> extract_variables("abc")
        []

    """
    # TODO: change variable notation from $var to {{var}}
    try:
        return re.findall(variable_regexp, content)
    except TypeError:
        return []


def extract_functions(content):
    """extract all functions from string content, which are in format ${fun()}

    Args:
        content (str): string content

    Returns:
        list: functions list extracted from string content

    Examples:
        >>> extract_functions("${func(5)}")
        ["func(5)"]

        >>> extract_functions("${func(a=1, b=2)}")
        ["func(a=1, b=2)"]

        >>> extract_functions("/api/1000?_t=${get_timestamp()}")
        ["get_timestamp()"]

        >>> extract_functions("/api/${add(1, 2)}")
        ["add(1, 2)"]

        >>> extract_functions("/api/${add(1, 2)}?_t=${get_timestamp()}")
        ["add(1, 2)", "get_timestamp()"]

    """
    try:
        return re.findall(function_regexp, content)
    except TypeError:
        return []


def parse_function(content):
    """parse function name and args from string content.

    Args:
        content (str): string content

    Returns:
        dict: function meta dict

            {
                "func_name": "xxx",
                "args": [],
                "kwargs": {}
            }

    Examples:
        >>> parse_function("func()")
        {'func_name': 'func', 'args': [], 'kwargs': {}}

        >>> parse_function("func(5)")
        {'func_name': 'func', 'args': [5], 'kwargs': {}}

        >>> parse_function("func(1, 2)")
        {'func_name': 'func', 'args': [1, 2], 'kwargs': {}}

        >>> parse_function("func(a=1, b=2)")
        {'func_name': 'func', 'args': [], 'kwargs': {'a': 1, 'b': 2}}

        >>> parse_function("func(1, 2, a=3, b=4)")
        {'func_name': 'func', 'args': [1, 2], 'kwargs': {'a':3, 'b':4}}

    """
    matched = function_regexp_compile.match(content)
    if not matched:
        raise exceptions.FunctionNotFound(f"{content} not found!")

    function_meta = {"func_name": matched.group(1), "args": [], "kwargs": {}}

    args_str = matched.group(2).strip()
    if args_str == "":
        return function_meta

    args_list = args_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


def parse_validator(validator):
    """parse validator, validator maybe in two format
    @param (dict) validator
        format1: this is kept for compatiblity with the previous versions.
            {"check": "status_code", "comparator": "eq", "expect": 201}
            {"check": "$resp_body_success", "comparator": "eq", "expect": True}
        format2: recommended new version
            {'eq': ['status_code', 201]}
            {'eq': ['$resp_body_success', True]}
    @return (dict) validator info
        {
            "check": "status_code",
            "expect": 201,
            "comparator": "eq"
        }
    """
    if not isinstance(validator, dict):
        raise exceptions.ParamsError(f"invalid validator: {validator}")

    if "check" in validator and len(validator) > 1:
        # format1
        check_item = validator.get("check")

        if "expect" in validator:
            expect_value = validator.get("expect")
        elif "expected" in validator:
            expect_value = validator.get("expected")
        else:
            raise exceptions.ParamsError(f"invalid validator: {validator}")

        comparator = validator.get("comparator", "eq")

    elif len(validator) == 1:
        # format2
        comparator = list(validator.keys())[0]
        compare_values: list = validator[comparator]

        if len(compare_values) == 2:
            compare_values.append("")

        if not isinstance(compare_values, list) or len(compare_values) != 3:
            raise exceptions.ParamsError(f"invalid validator: {validator}")

        if comparator in ("list_any_item_contains", "list_all_item_contains"):
            # list item比较器特殊检查
            if len(compare_values[1].split(" ")) != 3:
                msg = f"{compare_values} 是错误的表达式, 正确的期望值表达式比如:k = v,等号前后要有空格符"
                raise exceptions.ExpectValueParseFailure(msg)

        check_item, expect_value, desc = compare_values

    else:
        raise exceptions.ParamsError(f"invalid validator: {validator}")

    return {
        "check": check_item,
        "expect": expect_value,
        "comparator": comparator,
        "desc": desc,
    }


def substitute_variables(content, variables_mapping):
    """substitute variables in content with variables_mapping

    Args:
        content (str/dict/list/numeric/bool/type): content to be substituted.
        variables_mapping (dict): variables mapping.

    Returns:
        substituted content.

    Examples:
        >>> content = {
                'request': {
                    'url': '/api/users/$uid',
                    'headers': {'token': '$token'}
                }
            }
        >>> variables_mapping = {"$uid": 1000}
        >>> substitute_variables(content, variables_mapping)
            {
                'request': {
                    'url': '/api/users/1000',
                    'headers': {'token': '$token'}
                }
            }

    """
    if isinstance(content, (list, set, tuple)):
        return [substitute_variables(item, variables_mapping) for item in content]

    if isinstance(content, dict):
        substituted_data = {}
        for key, value in content.items():
            eval_key = substitute_variables(key, variables_mapping)
            eval_value = substitute_variables(value, variables_mapping)
            substituted_data[eval_key] = eval_value

        return substituted_data

    if isinstance(content, basestring):
        # content is in string format here
        for var, value in variables_mapping.items():
            if content == var:
                # content is a variable
                content = value
            else:
                if not isinstance(value, str):
                    value = builtin_str(value)
                content = content.replace(var, value)

    return content


def parse_parameters(parameters, variables_mapping, functions_mapping):
    """parse parameters and generate cartesian product.

    Args:
        parameters (list) parameters: parameter name and value in list
            parameter value may be in three types:
                (1) data list, e.g. ["iOS/10.1", "iOS/10.2", "iOS/10.3"]
                (2) call built-in parameterize function, "${parameterize(account.csv)}"
                (3) call custom function in debugtalk.py, "${gen_app_version()}"

        variables_mapping (dict): variables mapping loaded from debugtalk.py
        functions_mapping (dict): functions mapping loaded from debugtalk.py

    Returns:
        list: cartesian product list

    Examples:
        >>> parameters = [
            {"user_agent": ["iOS/10.1", "iOS/10.2", "iOS/10.3"]},
            {"username-password": "${parameterize(account.csv)}"},
            {"app_version": "${gen_app_version()}"}
        ]
        >>> parse_parameters(parameters)

    """
    parsed_parameters_list = []
    for parameter in parameters:
        parameter_name, parameter_content = list(parameter.items())[0]
        parameter_name_list = parameter_name.split("-")

        if isinstance(parameter_content, list):
            # (1) data list
            # e.g. {"app_version": ["2.8.5", "2.8.6"]}
            #       => [{"app_version": "2.8.5", "app_version": "2.8.6"}]
            # e.g. {"username-password": [["user1", "111111"], ["test2", "222222"]}
            #       => [{"username": "user1", "password": "111111"}, {"username": "user2", "password": "222222"}]
            parameter_content_list = []
            for parameter_item in parameter_content:
                if not isinstance(parameter_item, (list, tuple)):
                    # "2.8.5" => ["2.8.5"]
                    parameter_item = [parameter_item]

                # ["app_version"], ["2.8.5"] => {"app_version": "2.8.5"}
                # ["username", "password"], ["user1", "111111"] => {"username": "user1", "password": "111111"}
                parameter_content_dict = dict(zip(parameter_name_list, parameter_item))

                parameter_content_list.append(parameter_content_dict)
        else:
            # (2) & (3)
            parsed_parameter_content = parse_data(parameter_content, variables_mapping, functions_mapping)
            # e.g. [{'app_version': '2.8.5'}, {'app_version': '2.8.6'}]
            # e.g. [{"username": "user1", "password": "111111"}, {"username": "user2", "password": "222222"}]
            if not isinstance(parsed_parameter_content, list):
                raise exceptions.ParamsError("parameters syntax error!")

            parameter_content_list = [
                # get subset by parameter name
                {key: parameter_item[key] for key in parameter_name_list}
                for parameter_item in parsed_parameter_content
            ]

        parsed_parameters_list.append(parameter_content_list)

    return utils.gen_cartesian_product(*parsed_parameters_list)


###############################################################################
##  parse content with variables and functions mapping
###############################################################################


def get_builtin_item(item_type, item_name):
    """

    Args:
        item_type (enum): "variables" or "functions"
        item_name (str): variable name or function name

    Returns:
        variable or function with the name of item_name

    """
    # override built_in module with debugtalk.py module
    from httprunner import loader

    built_in_module = loader.load_builtin_module()

    if item_type == "variables":
        try:
            return built_in_module["variables"][item_name]
        except KeyError:
            logger.error(
                "variables_mapping and built_in_module, not found variable: %s",
                item_name,
                exc_info=True,
            )
            raise exceptions.VariableNotFound(
                "variables_mapping and built_in_module, not found variable: %s",
                item_name,
            )
    else:
        # item_type == "functions":
        try:
            return built_in_module["functions"][item_name]
        except KeyError:
            raise exceptions.FunctionNotFound(f"{item_name} is not found.")


def get_mapping_variable(variable_name, variables_mapping):
    """get variable from variables_mapping.

    Args:
        variable_name (str): variable name
        variables_mapping (dict): variables mapping

    Returns:
        mapping variable value.

    Raises:
        exceptions.VariableNotFound: variable is not found.

    """
    if variable_name in variables_mapping:
        return variables_mapping[variable_name]
    else:
        return get_builtin_item("variables", variable_name)


def get_mapping_function(function_name, functions_mapping):
    """get function from functions_mapping,
        if not found, then try to check if builtin function.

    Args:
        variable_name (str): variable name
        variables_mapping (dict): variables mapping

    Returns:
        mapping function object.

    Raises:
        exceptions.FunctionNotFound: function is neither defined in debugtalk.py nor builtin.

    """
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    try:
        return get_builtin_item("functions", function_name)
    except exceptions.FunctionNotFound:
        pass

    try:
        # check if builtin functions
        item_func = eval(function_name)
        if callable(item_func):
            # is builtin function
            return item_func
    except (NameError, TypeError):
        # is not builtin function
        raise exceptions.FunctionNotFound(f"{function_name} is not found.")


def parse_string_functions(content, variables_mapping, functions_mapping):
    """parse string content with functions mapping.

    Args:
        content (str): string content to be parsed.
        variables_mapping (dict): variables mapping.
        functions_mapping (dict): functions mapping.

    Returns:
        str: parsed string content.

    Examples:
        >>> content = "abc${add_one(3)}def"
        >>> functions_mapping = {"add_one": lambda x: x + 1}
        >>> parse_string_functions(content, functions_mapping)
            "abc4def"

    """
    functions_list = extract_functions(content)
    for func_content in functions_list:
        function_meta = parse_function(func_content)
        func_name = function_meta["func_name"]

        args = function_meta.get("args", [])
        kwargs = function_meta.get("kwargs", {})
        args = parse_data(args, variables_mapping, functions_mapping)
        kwargs = parse_data(kwargs, variables_mapping, functions_mapping)

        if func_name in ["parameterize", "P"]:
            from httprunner import loader

            eval_value = loader.load_csv_file(*args, **kwargs)
        else:
            func = get_mapping_function(func_name, functions_mapping)
            eval_value = func(*args, **kwargs)

        func_content = "${" + func_content + "}"
        if func_content == content:
            # content is a function, e.g. "${add_one(3)}"
            content = eval_value
        else:
            # content contains one or many functions, e.g. "abc${add_one(3)}def"
            content = content.replace(func_content, str(eval_value), 1)

    return content


def parse_string_variables(content, variables_mapping):
    """parse string content with variables mapping.

    Args:
        content (str): string content to be parsed.
        variables_mapping (dict): variables mapping.

    Returns:
        str: parsed string content.

    Examples:
        >>> content = "/api/users/$uid"
        >>> variables_mapping = {"$uid": 1000}
        >>> parse_string_variables(content, variables_mapping)
            "/api/users/1000"

    """
    variables_list = extract_variables(content)
    for variable_name in variables_list:
        variable_value = get_mapping_variable(variable_name, variables_mapping)

        # TODO: replace variable label from $var to {{var}}
        if f"${variable_name}" == content:
            # content is a variable
            content = variable_value
        else:
            # content contains one or several variables
            if not isinstance(variable_value, str):
                variable_value = builtin_str(variable_value)

            content = content.replace(f"${variable_name}", variable_value, 1)

    return content


def parse_function_params(params) -> dict:
    """parse function params to args and kwargs.
    Args:
        params (str): function param in string
    Returns:
        dict: function meta dict
            {
                "args": [],
                "kwargs": {}
            }
    Examples:
        >>> parse_function_params("")
        {'args': [], 'kwargs': {}}
        >>> parse_function_params("5")
        {'args': [5], 'kwargs': {}}
        >>> parse_function_params("1, 2")
        {'args': [1, 2], 'kwargs': {}}
        >>> parse_function_params("a=1, b=2")
        {'args': [], 'kwargs': {'a': 1, 'b': 2}}
        >>> parse_function_params("1, 2, a=3, b=4")
        {'args': [1, 2], 'kwargs': {'a':3, 'b':4}}
    """
    function_meta = {"args": [], "kwargs": {}}

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


def _format_func(func_name, parsed_args, parsed_kwargs):
    args_str = ", ".join(map(str, parsed_args))
    kwargs_str = ",".join(f"{k}={v}" for k, v in parsed_kwargs.items())

    if not args_str and not kwargs_str:
        return f"{func_name}()"
    elif not args_str:
        return f"{func_name}({kwargs_str})"
    elif not kwargs_str:
        return f"{func_name}({args_str})"
    else:
        return f"{func_name}({args_str}, {kwargs_str})"


def parse_string(
    raw_string,
    variables_mapping,
    functions_mapping,
):
    """parse string content with variables and functions mapping.
    Args:
        raw_string: raw string content to be parsed.
        variables_mapping: variables mapping.
        functions_mapping: functions mapping.
    Returns:
        str: parsed string content.
    Examples:
        >>> raw_string = "abc${add_one($num)}def"
        >>> variables_mapping = {"num": 3}
        >>> functions_mapping = {"add_one": lambda x: x + 1}
        >>> parse_string(raw_string, variables_mapping, functions_mapping)
            "abc4def"
    """
    try:
        match_start_position = raw_string.index("$", 0)
        parsed_string = raw_string[0:match_start_position]
    except ValueError:
        parsed_string = raw_string
        return parsed_string

    while match_start_position < len(raw_string):
        # Notice: notation priority
        # $$ > ${func($a, $b)} > $var

        # search $$
        dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            parsed_string += "$"
            continue

        # search function like ${func($a, $b)}
        func_match = function_regex_compile.match(raw_string, match_start_position)
        if func_match:
            func_name = func_match.group(1)
            func = get_mapping_function(func_name, functions_mapping)

            func_params_str = func_match.group(2)
            logger.info("raw func_params_str:  %s", func_params_str)
            function_meta = parse_function_params(func_params_str)
            logger.info("function_meta: %s", function_meta)
            args = function_meta["args"]
            kwargs = function_meta["kwargs"]
            parsed_args = parse_data(args, variables_mapping, functions_mapping)
            parsed_kwargs = parse_data(kwargs, variables_mapping, functions_mapping)
            try:
                logger.info(
                    "parsed func: %s",
                    _format_func(func_name, parsed_args, parsed_kwargs),
                )
                func_eval_value = func(*parsed_args, **parsed_kwargs)
                logger.info("func return value: %s", func_eval_value)
            except Exception as ex:
                logger.error(
                    f"call function error:\n"
                    f"func_name: {func_name}\n"
                    f"args: {parsed_args}\n"
                    f"kwargs: {parsed_kwargs}\n"
                    f"{type(ex).__name__}: {ex}"
                )
                raise

            func_raw_str = "${" + func_name + f"({func_params_str})" + "}"
            if func_raw_str == raw_string:
                # raw_string is a function, e.g. "${add_one(3)}", return its eval value directly
                return func_eval_value

            # raw_string contains one or many functions, e.g. "abc${add_one(3)}def"
            parsed_string += str(func_eval_value)
            match_start_position = func_match.end()
            continue

        # search variable like ${var} or $var
        var_match = variable_regex_compile.match(raw_string, match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            var_value = get_mapping_variable(var_name, variables_mapping)

            if f"${var_name}" == raw_string or "${" + var_name + "}" == raw_string:
                # raw_string is a variable, $var or ${var}, return its value directly
                return var_value

            # raw_string contains one or many variables, e.g. "abc${var}def"
            parsed_string += str(var_value)
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
            remain_string = raw_string[curr_position:match_start_position]
        except ValueError:
            remain_string = raw_string[curr_position:]
            # break while loop
            match_start_position = len(raw_string)

        parsed_string += remain_string

    return parsed_string


def parse_data(content, variables_mapping=None, functions_mapping=None):
    """parse content with variables mapping

    Args:
        content (str/dict/list/numeric/bool/type): content to be parsed
        variables_mapping (dict): variables mapping.
        functions_mapping (dict): functions mapping.

    Returns:
        parsed content.

    Examples:
        >>> content = {
                'request': {
                    'url': '/api/users/$uid',
                    'headers': {'token': '$token'}
                }
            }
        >>> variables_mapping = {"uid": 1000, "token": "abcdef"}
        >>> parse_data(content, variables_mapping)
            {
                'request': {
                    'url': '/api/users/1000',
                    'headers': {'token': 'abcdef'}
                }
            }

    """
    # TODO: refactor type check
    if content is None or isinstance(content, (numeric_types, bool, type)):
        return content

    if isinstance(content, (list, set, tuple)):
        return [parse_data(item, variables_mapping, functions_mapping) for item in content]

    if isinstance(content, dict):
        parsed_content = {}
        for key, value in content.items():
            parsed_key = parse_data(key, variables_mapping, functions_mapping)
            parsed_value = parse_data(value, variables_mapping, functions_mapping)
            parsed_content[parsed_key] = parsed_value

        return parsed_content

    if isinstance(content, basestring):
        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}
        has_variable_match = variable_regex_compile.search(content)
        if has_variable_match:
            logger.info("source string content: %s", content)
        content = parse_string(content, variables_mapping, functions_mapping)
        if has_variable_match:
            logger.info("parsed string content: %s", content)
        # replace $$ notation with $ and consider it as normal char.
        # if '$$' in content:
        #     return content.replace("$$", "$")

        # content is in string format here
        # variables_mapping = variables_mapping or {}
        # functions_mapping = functions_mapping or {}
        # content = content.strip()

        # # replace functions with evaluated value
        # # Notice: _eval_content_functions must be called before _eval_content_variables
        # content = parse_string_functions(content, variables_mapping, functions_mapping)
        #
        # # replace variables with binding value
        # content = parse_string_variables(content, variables_mapping)

    return content


def parse_tests(testcases, variables_mapping=None):
    """parse testcases configs, including variables/parameters/name/request.

    Args:
        testcases (list): testcase list, with config unparsed.
            [
                {   # testcase data structure
                    "config": {
                        "name": "desc1",
                        "path": "testcase1_path",
                        "variables": [],         # optional
                        "request": {}            # optional
                        "refs": {
                            "debugtalk": {
                                "variables": {},
                                "functions": {}
                            },
                            "env": {},
                            "def-api": {},
                            "def-testcase": {}
                        }
                    },
                    "teststeps": [
                        # teststep data structure
                        {
                            'name': 'test step desc2',
                            'variables': [],    # optional
                            'extract': [],      # optional
                            'validate': [],
                            'request': {},
                            'function_meta': {}
                        },
                        teststep2   # another teststep dict
                    ]
                },
                testcase_dict_2     # another testcase dict
            ]
        variables_mapping (dict): if variables_mapping is specified, it will override variables in config block.

    Returns:
        list: parsed testcases list, with config variables/parameters/name/request parsed.

    """
    variables_mapping = variables_mapping or {}
    parsed_testcases_list = []

    for testcase in testcases:
        testcase_config = testcase.setdefault("config", {})
        project_mapping = testcase_config.pop(
            "refs",
            {
                "debugtalk": {"variables": {}, "functions": {}},
                "env": {},
                "def-api": {},
                "def-testcase": {},
            },
        )

        # parse config parameters
        config_parameters = testcase_config.pop("parameters", [])
        cartesian_product_parameters_list = parse_parameters(
            config_parameters,
            project_mapping["debugtalk"]["variables"],
            project_mapping["debugtalk"]["functions"],
        ) or [{}]

        for parameter_mapping in cartesian_product_parameters_list:
            testcase_dict = utils.deepcopy_dict(testcase)
            config = testcase_dict.get("config")

            # parse config variables
            raw_config_variables = config.get("variables", [])
            parsed_config_variables = parse_data(
                raw_config_variables,
                project_mapping["debugtalk"]["variables"],
                project_mapping["debugtalk"]["functions"],
            )

            # priority: passed in > debugtalk.py > parameters > variables
            # override variables mapping with parameters mapping
            config_variables = utils.override_mapping_list(parsed_config_variables, parameter_mapping)
            # merge debugtalk.py module variables
            config_variables.update(project_mapping["debugtalk"]["variables"])
            # override variables mapping with passed in variables_mapping
            config_variables = utils.override_mapping_list(config_variables, variables_mapping)

            testcase_dict["config"]["variables"] = config_variables

            # parse config name
            testcase_dict["config"]["name"] = parse_data(
                testcase_dict["config"].get("name", ""),
                config_variables,
                project_mapping["debugtalk"]["functions"],
            )

            # parse config request
            testcase_dict["config"]["request"] = parse_data(
                testcase_dict["config"].get("request", {}),
                config_variables,
                project_mapping["debugtalk"]["functions"],
            )

            # put loaded project functions to config
            testcase_dict["config"]["functions"] = project_mapping["debugtalk"]["functions"]
            parsed_testcases_list.append(testcase_dict)

    return parsed_testcases_list
