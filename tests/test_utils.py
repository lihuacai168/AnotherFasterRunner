import collections
from unittest.mock import MagicMock, patch

import pytest

from fastrunner.utils.parser import Format, Parse
from fastrunner.utils.response import ErrorMsg, StandResponse
from fastrunner.utils.tree import get_all_ycatid, get_tree_max_id, get_tree_ycatid_mapping


class TestTreeUtils:
    """Test tree utility functions"""
    
    def test_get_tree_max_id_empty_tree(self):
        """Test get_tree_max_id with empty tree"""
        result = get_tree_max_id([])
        assert result == 0
        
    def test_get_tree_max_id_single_node(self):
        """Test get_tree_max_id with single node"""
        tree = [{"id": 5, "children": []}]
        result = get_tree_max_id(tree)
        assert result == 5
        
    def test_get_tree_max_id_nested_tree(self):
        """Test get_tree_max_id with nested structure"""
        tree = [
            {
                "id": 1,
                "children": [
                    {"id": 3, "children": []},
                    {"id": 7, "children": [{"id": 10, "children": []}]}
                ]
            },
            {
                "id": 2,
                "children": [{"id": 5, "children": []}]
            }
        ]
        result = get_tree_max_id(tree)
        assert result == 10
        
    def test_get_tree_max_id_complex_tree(self):
        """Test get_tree_max_id with complex nested structure"""
        tree = [
            {
                "id": 15,
                "children": [
                    {
                        "id": 8,
                        "children": [
                            {"id": 25, "children": []},
                            {"id": 12, "children": []}
                        ]
                    }
                ]
            }
        ]
        result = get_tree_max_id(tree)
        assert result == 25
        
    def test_get_all_ycatid_empty(self):
        """Test get_all_ycatid with empty input"""
        result = get_all_ycatid([])
        assert result == []
        
    def test_get_all_ycatid_no_yapi_catid(self):
        """Test get_all_ycatid with nodes that have no yapi_catid"""
        tree = [
            {"id": 1, "name": "node1", "children": []},
            {"id": 2, "name": "node2", "children": []}
        ]
        result = get_all_ycatid(tree)
        assert result == []
        
    def test_get_all_ycatid_with_yapi_catid(self):
        """Test get_all_ycatid with nodes that have yapi_catid"""
        tree = [
            {"id": 1, "yapi_catid": 100, "children": []},
            {"id": 2, "yapi_catid": 200, "children": [
                {"id": 3, "yapi_catid": 300, "children": []}
            ]}
        ]
        result = get_all_ycatid(tree)
        expected = [100, 200, 300]
        assert sorted(result) == sorted(expected)


class TestResponseUtils:
    """Test response utility classes and functions"""
    
    def test_error_msg_defaults(self):
        """Test ErrorMsg with default values"""
        error = ErrorMsg()
        assert error.code == "0001"
        assert error.msg == "成功"
        assert error.success is True
        
    def test_error_msg_custom_values(self):
        """Test ErrorMsg with custom values"""
        error = ErrorMsg(
            code="0102",
            msg="项目不存在",
            success=False
        )
        assert error.code == "0102"
        assert error.msg == "项目不存在"
        assert error.success is False
        
    def test_stand_response_creation(self):
        """Test StandResponse creation"""
        data = {"id": 1, "name": "test"}
        response = StandResponse[dict](
            code="0001",
            msg="成功",
            success=True,
            data=data
        )
        assert response.code == "0001"
        assert response.msg == "成功"
        assert response.success is True
        assert response.data == data


class TestParserUtils:
    """Test parser utility functions"""
    
    def test_format_initialization(self):
        """Test Format class initialization"""
        test_data = {"key": "value", "number": 123}
        formatter = Format(test_data)
        
        # Test that data is stored correctly
        assert hasattr(formatter, 'testcase')
        
    def test_parse_initialization(self):
        """Test Parse class initialization"""
        test_data = {"request": {"method": "GET", "url": "/test"}}
        parser = Parse(test_data)
        
        # Test that data is stored correctly
        assert hasattr(parser, 'testcase')
        
    @patch('fastrunner.utils.parser.Format')
    def test_format_mock_usage(self, mock_format):
        """Test Format class with mocking"""
        mock_instance = MagicMock()
        mock_format.return_value = mock_instance
        
        test_data = {"test": "data"}
        formatter = Format(test_data)
        
        mock_format.assert_called_once_with(test_data)
        
    @patch('fastrunner.utils.parser.Parse')
    def test_parse_mock_usage(self, mock_parse):
        """Test Parse class with mocking"""
        mock_instance = MagicMock()
        mock_parse.return_value = mock_instance
        
        test_data = {"request": {"method": "POST"}}
        parser = Parse(test_data)
        
        mock_parse.assert_called_once_with(test_data)


class TestUtilityFunctionEdgeCases:
    """Test edge cases and error conditions in utility functions"""
    
    def test_get_tree_max_id_malformed_tree(self):
        """Test get_tree_max_id with malformed tree structure"""
        # Tree with missing children key
        with pytest.raises((KeyError, AttributeError)):
            tree = [{"id": 1}]  # Missing children
            get_tree_max_id(tree)
            
    def test_get_tree_max_id_invalid_id_type(self):
        """Test get_tree_max_id with invalid id types"""
        # Tree with string id (should be handled or raise error)
        tree = [{"id": "invalid", "children": []}]
        with pytest.raises((TypeError, ValueError)):
            get_tree_max_id(tree)
            
    def test_get_tree_max_id_negative_ids(self):
        """Test get_tree_max_id with negative ids"""
        tree = [
            {"id": -5, "children": []},
            {"id": -10, "children": []},
            {"id": 3, "children": []}
        ]
        result = get_tree_max_id(tree)
        assert result == 3  # Should return the maximum value
        
    def test_get_all_ycatid_mixed_data(self):
        """Test get_all_ycatid with mixed data types"""
        tree = [
            {"id": 1, "yapi_catid": 100, "children": []},
            {"id": 2, "children": []},  # No yapi_catid
            {"id": 3, "yapi_catid": None, "children": []},  # None yapi_catid
            {"id": 4, "yapi_catid": 200, "children": []}
        ]
        result = get_all_ycatid(tree)
        # Should only include valid yapi_catid values
        assert 100 in result
        assert 200 in result
        assert None not in result
        
    def test_response_constants_exist(self):
        """Test that common response constants are defined"""
        from fastrunner.utils import response
        
        # Test some common response constants
        assert hasattr(response, 'PROJECT_EXISTS')
        assert hasattr(response, 'PROJECT_NOT_EXISTS')
        assert hasattr(response, 'SYSTEM_ERROR')
        assert hasattr(response, 'API_ADD_SUCCESS')
        
        # Test structure of response constants
        assert response.PROJECT_EXISTS['success'] is False
        assert 'code' in response.PROJECT_EXISTS
        assert 'msg' in response.PROJECT_EXISTS
        
    def test_tree_function_performance(self):
        """Test tree function performance with large tree"""
        # Create a large tree structure
        large_tree = []
        for i in range(100):
            node = {
                "id": i,
                "children": [
                    {"id": i * 1000 + j, "children": []}
                    for j in range(10)
                ]
            }
            large_tree.append(node)
            
        # Should complete in reasonable time
        result = get_tree_max_id(large_tree)
        assert result == 99990  # 99 * 1000 + 9
        
    def test_breadth_first_vs_recursive_consistency(self):
        """Test that breadth-first and recursive approaches give same result"""
        tree = [
            {
                "id": 1,
                "children": [
                    {"id": 5, "children": [{"id": 20, "children": []}]},
                    {"id": 3, "children": []}
                ]
            },
            {
                "id": 10,
                "children": [{"id": 15, "children": []}]
            }
        ]
        
        # Test current implementation
        result_bfs = get_tree_max_id(tree)
        
        # Test old recursive implementation (if available)
        try:
            from fastrunner.utils.tree import get_tree_max_id_old
            result_recursive = get_tree_max_id_old(tree, [])
            assert result_bfs == result_recursive
        except ImportError:
            # Old function might not be available, skip this comparison
            pass
            
        assert result_bfs == 20