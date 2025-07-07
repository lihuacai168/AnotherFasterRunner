import pytest

from fastrunner.utils.safe_json_parser import safe_json_loads, safe_literal_eval


class TestSafeJsonParser:
    """Test safe JSON parser utilities"""
    
    def test_safe_json_loads_valid_json(self):
        """Test parsing valid JSON strings"""
        assert safe_json_loads('{"key": "value"}') == {"key": "value"}
        assert safe_json_loads('[1, 2, 3]') == [1, 2, 3]
        assert safe_json_loads('null') is None
        assert safe_json_loads('true') is True
        assert safe_json_loads('false') is False
        assert safe_json_loads('123') == 123
        assert safe_json_loads('"string"') == "string"
    
    def test_safe_json_loads_empty_input(self):
        """Test handling empty input"""
        assert safe_json_loads('') == {}
        assert safe_json_loads(None) == {}
    
    def test_safe_json_loads_already_parsed(self):
        """Test handling already parsed objects"""
        dict_obj = {"key": "value"}
        assert safe_json_loads(dict_obj) == dict_obj
        
        list_obj = [1, 2, 3]
        assert safe_json_loads(list_obj) == list_obj
    
    def test_safe_json_loads_python_dict_string(self):
        """Test parsing Python dict/list strings"""
        assert safe_json_loads("{'key': 'value'}") == {"key": "value"}
        assert safe_json_loads("{'bool': True, 'none': None}") == {"bool": True, "none": None}
        assert safe_json_loads("[1, 2, 'three']") == [1, 2, "three"]
    
    def test_safe_json_loads_invalid_json(self):
        """Test handling invalid JSON"""
        with pytest.raises(ValueError, match="Invalid JSON data"):
            safe_json_loads("{invalid json}")
        
        with pytest.raises(ValueError, match="Invalid JSON data"):
            safe_json_loads("not json at all")
    
    def test_safe_literal_eval_valid_literals(self):
        """Test evaluating valid Python literals"""
        assert safe_literal_eval("{'key': 'value'}") == {"key": "value"}
        assert safe_literal_eval("[1, 2, 3]") == [1, 2, 3]
        assert safe_literal_eval("(1, 2, 3)") == (1, 2, 3)
        assert safe_literal_eval("{1, 2, 3}") == {1, 2, 3}
        assert safe_literal_eval("True") is True
        assert safe_literal_eval("False") is False
        assert safe_literal_eval("None") is None
        assert safe_literal_eval("123") == 123
        assert safe_literal_eval("3.14") == 3.14
        assert safe_literal_eval("'string'") == "string"
    
    def test_safe_literal_eval_empty_input(self):
        """Test handling empty input"""
        assert safe_literal_eval('') is None
        assert safe_literal_eval(None) is None
    
    def test_safe_literal_eval_non_string_input(self):
        """Test handling non-string input"""
        assert safe_literal_eval(123) == 123
        assert safe_literal_eval([1, 2, 3]) == [1, 2, 3]
    
    def test_safe_literal_eval_unsafe_expressions(self):
        """Test rejecting unsafe expressions"""
        with pytest.raises(ValueError, match="Invalid literal"):
            safe_literal_eval("__import__('os').system('ls')")
        
        with pytest.raises(ValueError, match="Invalid literal"):
            safe_literal_eval("lambda x: x + 1")
        
        with pytest.raises(ValueError, match="Invalid literal"):
            safe_literal_eval("1 + 1")
    
    def test_safe_literal_eval_complex_literals(self):
        """Test evaluating complex nested literals"""
        complex_literal = "{'users': [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}], 'count': 2}"
        expected = {'users': [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}], 'count': 2}
        assert safe_literal_eval(complex_literal) == expected