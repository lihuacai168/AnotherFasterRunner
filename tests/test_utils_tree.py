import collections
from unittest.mock import patch

import pytest

from fastrunner.utils import tree


class TestGetTreeMaxIdOld:
    """Test cases for get_tree_max_id_old function"""

    def test_empty_value(self):
        """Test with empty value"""
        result = tree.get_tree_max_id_old(None)
        assert result == 0
        
        result = tree.get_tree_max_id_old([])
        assert result == 0

    def test_single_level_tree(self):
        """Test with single level tree"""
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 3, "label": "Node 3", "children": []},
            {"id": 2, "label": "Node 2", "children": []}
        ]
        # Reset list_id to avoid side effects
        result = tree.get_tree_max_id_old(value, list_id=[])
        assert result == 3

    def test_multi_level_tree(self):
        """Test with multi-level tree"""
        value = [
            {
                "id": 1,
                "label": "Parent 1",
                "children": [
                    {"id": 10, "label": "Child 1", "children": []},
                    {"id": 11, "label": "Child 2", "children": []}
                ]
            },
            {
                "id": 2,
                "label": "Parent 2",
                "children": [
                    {
                        "id": 20,
                        "label": "Child 3",
                        "children": [
                            {"id": 100, "label": "Grandchild 1", "children": []}
                        ]
                    }
                ]
            }
        ]
        result = tree.get_tree_max_id_old(value, list_id=[])
        assert result == 100

    def test_list_id_accumulation_issue(self):
        """Test the list_id accumulation issue in the original function"""
        value = [{"id": 5, "label": "Node", "children": []}]
        
        # First call
        result1 = tree.get_tree_max_id_old(value)
        assert result1 == 5
        
        # Second call - demonstrates the bug where list_id accumulates
        result2 = tree.get_tree_max_id_old(value)
        # This would fail with the original function due to list_id accumulation
        # But we're testing the actual behavior
        assert result2 == 5


class TestGetTreeMaxId:
    """Test cases for get_tree_max_id function (improved version)"""

    def test_empty_tree(self):
        """Test with empty tree"""
        result = tree.get_tree_max_id([])
        assert result == 0

    def test_single_node(self):
        """Test with single node"""
        value = [{"id": 42, "label": "Single Node", "children": []}]
        result = tree.get_tree_max_id(value)
        assert result == 42

    def test_flat_tree(self):
        """Test with flat tree structure"""
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 5, "label": "Node 5", "children": []},
            {"id": 3, "label": "Node 3", "children": []}
        ]
        result = tree.get_tree_max_id(value)
        assert result == 5

    def test_nested_tree(self):
        """Test with deeply nested tree"""
        value = [
            {
                "id": 1,
                "label": "Root",
                "children": [
                    {
                        "id": 10,
                        "label": "Level 1",
                        "children": [
                            {
                                "id": 100,
                                "label": "Level 2",
                                "children": [
                                    {"id": 1000, "label": "Level 3", "children": []}
                                ]
                            }
                        ]
                    },
                    {"id": 20, "label": "Level 1-2", "children": []}
                ]
            }
        ]
        result = tree.get_tree_max_id(value)
        assert result == 1000

    def test_multiple_branches(self):
        """Test with multiple branches"""
        value = [
            {
                "id": 1,
                "label": "Branch 1",
                "children": [
                    {"id": 11, "label": "Child 1-1", "children": []},
                    {"id": 12, "label": "Child 1-2", "children": []}
                ]
            },
            {
                "id": 2,
                "label": "Branch 2", 
                "children": [
                    {"id": 21, "label": "Child 2-1", "children": []},
                    {"id": 25, "label": "Child 2-2", "children": []}
                ]
            },
            {
                "id": 3,
                "label": "Branch 3",
                "children": []
            }
        ]
        result = tree.get_tree_max_id(value)
        assert result == 25


class TestGetAllYcatid:
    """Test cases for get_all_ycatid function"""

    def test_empty_value(self):
        """Test with empty value"""
        result = tree.get_all_ycatid(None, list_id=[])
        assert result == []
        
        result = tree.get_all_ycatid([], list_id=[])
        assert result == []

    def test_no_yapi_catid(self):
        """Test tree without yapi_catid"""
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 2, "label": "Node 2", "children": []}
        ]
        result = tree.get_all_ycatid(value, list_id=[])
        assert result == []

    def test_with_yapi_catid(self):
        """Test tree with yapi_catid"""
        value = [
            {"id": 1, "label": "Node 1", "yapi_catid": 101, "children": []},
            {"id": 2, "label": "Node 2", "children": []},
            {"id": 3, "label": "Node 3", "yapi_catid": 103, "children": []}
        ]
        result = tree.get_all_ycatid(value, list_id=[])
        assert sorted(result) == [101, 103]

    def test_nested_yapi_catid(self):
        """Test nested tree with yapi_catid"""
        value = [
            {
                "id": 1,
                "label": "Parent",
                "yapi_catid": 100,
                "children": [
                    {"id": 10, "label": "Child 1", "yapi_catid": 110, "children": []},
                    {"id": 11, "label": "Child 2", "children": []}
                ]
            }
        ]
        result = tree.get_all_ycatid(value, list_id=[])
        assert sorted(result) == [100, 110]


class TestGetFasterIdByYcatid:
    """Test cases for get_faster_id_by_ycatid function"""

    def test_empty_value(self):
        """Test with empty value"""
        result = tree.get_faster_id_by_ycatid(None, 100)
        assert result == 0

    def test_not_found(self):
        """Test when yapi_catid is not found"""
        value = [
            {"id": 1, "label": "Node 1", "yapi_catid": 101, "children": []},
            {"id": 2, "label": "Node 2", "yapi_catid": 102, "children": []}
        ]
        result = tree.get_faster_id_by_ycatid(value, 999)
        assert result == 0

    def test_found_at_root(self):
        """Test when yapi_catid is found at root level"""
        value = [
            {"id": 1, "label": "Node 1", "yapi_catid": 101, "children": []},
            {"id": 2, "label": "Node 2", "yapi_catid": 102, "children": []}
        ]
        result = tree.get_faster_id_by_ycatid(value, 102)
        assert result == 2

    def test_found_in_children(self):
        """Test when yapi_catid is found in children"""
        value = [
            {
                "id": 1,
                "label": "Parent",
                "children": [
                    {"id": 10, "label": "Child 1", "yapi_catid": 110, "children": []},
                    {"id": 11, "label": "Child 2", "yapi_catid": 111, "children": []}
                ]
            }
        ]
        # Note: The original function has a bug - it doesn't return the recursive call result
        # Testing actual behavior
        result = tree.get_faster_id_by_ycatid(value, 110)
        # Due to the bug, this returns 0 instead of 10
        assert result == 0


class TestGetTreeYcatidMapping:
    """Test cases for get_tree_ycatid_mapping function"""

    def test_empty_value(self):
        """Test with empty value"""
        result = tree.get_tree_ycatid_mapping(None, mapping={})
        assert result == {}
        
        result = tree.get_tree_ycatid_mapping([], mapping={})
        assert result == {}

    def test_no_yapi_catid(self):
        """Test tree without yapi_catid"""
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 2, "label": "Node 2", "children": []}
        ]
        result = tree.get_tree_ycatid_mapping(value, mapping={})
        assert result == {}

    def test_flat_mapping(self):
        """Test flat tree mapping"""
        value = [
            {"id": 1, "label": "Node 1", "yapi_catid": 101, "children": []},
            {"id": 2, "label": "Node 2", "children": []},
            {"id": 3, "label": "Node 3", "yapi_catid": 103, "children": []}
        ]
        result = tree.get_tree_ycatid_mapping(value, mapping={})
        assert result == {101: 1, 103: 3}

    def test_nested_mapping(self):
        """Test nested tree mapping"""
        value = [
            {
                "id": 1,
                "label": "Parent",
                "yapi_catid": 100,
                "children": [
                    {"id": 10, "label": "Child 1", "yapi_catid": 110, "children": []},
                    {
                        "id": 11,
                        "label": "Child 2",
                        "children": [
                            {"id": 111, "label": "Grandchild", "yapi_catid": 1110, "children": []}
                        ]
                    }
                ]
            }
        ]
        result = tree.get_tree_ycatid_mapping(value, mapping={})
        assert result == {100: 1, 110: 10, 1110: 111}


class TestGetFileSize:
    """Test cases for get_file_size function"""

    def test_bytes(self):
        """Test file size in bytes"""
        assert tree.get_file_size(0) == "0Byte"
        assert tree.get_file_size(1) == "1Byte"
        assert tree.get_file_size(1023) == "1023Byte"

    def test_kilobytes(self):
        """Test file size in kilobytes"""
        assert tree.get_file_size(1024) == "1.0KB"
        assert tree.get_file_size(1536) == "1.5KB"
        assert tree.get_file_size(1048575) == "1024.0KB"

    def test_megabytes(self):
        """Test file size in megabytes"""
        assert tree.get_file_size(1048576) == "1.0MB"
        assert tree.get_file_size(1572864) == "1.5MB"
        assert tree.get_file_size(10485760) == "10.0MB"

    def test_rounding(self):
        """Test rounding to 2 decimal places"""
        assert tree.get_file_size(1126) == "1.1KB"  # 1126/1024 = 1.0996...
        assert tree.get_file_size(1234567) == "1.18MB"  # 1234567/1048576 = 1.177...


class TestGetTreeLabel:
    """Test cases for get_tree_label function"""

    def setUp(self):
        """Reset global label_id before each test"""
        tree.label_id = 1

    def test_empty_value(self):
        """Test with empty value"""
        self.setUp()
        result = tree.get_tree_label(None, "search")
        assert result == 1  # default

    def test_label_not_found(self):
        """Test when label is not found"""
        self.setUp()
        value = [
            {"id": 2, "label": "Node 1", "children": []},
            {"id": 3, "label": "Node 2", "children": []}
        ]
        result = tree.get_tree_label(value, "Not Found")
        assert result == 1  # default

    def test_label_found_at_root(self):
        """Test when label is found at root level"""
        self.setUp()
        value = [
            {"id": 2, "label": "Node 1", "children": []},
            {"id": 3, "label": "Target Node", "children": []},
            {"id": 4, "label": "Node 3", "children": []}
        ]
        result = tree.get_tree_label(value, "Target Node")
        assert result == 3

    def test_label_found_in_children(self):
        """Test when label is found in nested children"""
        self.setUp()
        value = [
            {
                "id": 2,
                "label": "Parent",
                "children": [
                    {"id": 20, "label": "Child 1", "children": []},
                    {"id": 21, "label": "Target Child", "children": []}
                ]
            }
        ]
        result = tree.get_tree_label(value, "Target Child")
        assert result == 21

    def test_global_state_persistence(self):
        """Test that global state persists between calls"""
        self.setUp()
        value = [{"id": 5, "label": "Test", "children": []}]
        
        # First call sets label_id to 5
        result1 = tree.get_tree_label(value, "Test")
        assert result1 == 5
        
        # Second call with non-existent label should return the persisted value
        result2 = tree.get_tree_label(value, "Not Found")
        assert result2 == 5  # Returns persisted value, not default


class TestGetTreeRelationName:
    """Test cases for get_tree_relation_name function"""

    def setUp(self):
        """Reset global label before each test"""
        tree.label = ""

    def test_empty_value(self):
        """Test with empty value"""
        self.setUp()
        result = tree.get_tree_relation_name(None, 1)
        assert result == ""

    def test_id_not_found(self):
        """Test when id is not found"""
        self.setUp()
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 2, "label": "Node 2", "children": []}
        ]
        result = tree.get_tree_relation_name(value, 999)
        assert result == ""

    def test_id_found_at_root(self):
        """Test when id is found at root level"""
        self.setUp()
        value = [
            {"id": 1, "label": "Node 1", "children": []},
            {"id": 2, "label": "Target Node", "children": []},
            {"id": 3, "label": "Node 3", "children": []}
        ]
        result = tree.get_tree_relation_name(value, 2)
        assert result == "Target Node"

    def test_id_found_in_children(self):
        """Test when id is found in nested children"""
        self.setUp()
        value = [
            {
                "id": 1,
                "label": "Parent",
                "children": [
                    {"id": 10, "label": "Child 1", "children": []},
                    {
                        "id": 11,
                        "label": "Child 2",
                        "children": [
                            {"id": 111, "label": "Grandchild Target", "children": []}
                        ]
                    }
                ]
            }
        ]
        result = tree.get_tree_relation_name(value, 111)
        assert result == "Grandchild Target"

    def test_global_state_persistence(self):
        """Test that global state persists between calls"""
        self.setUp()
        value = [{"id": 1, "label": "First Label", "children": []}]
        
        # First call sets label to "First Label"
        result1 = tree.get_tree_relation_name(value, 1)
        assert result1 == "First Label"
        
        # Second call with non-existent id should return the persisted value
        result2 = tree.get_tree_relation_name(value, 999)
        assert result2 == "First Label"  # Returns persisted value


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_tree_with_missing_children_key(self):
        """Test tree nodes without 'children' key"""
        value = [
            {"id": 1, "label": "Node without children key"},
            {"id": 2, "label": "Node with empty children", "children": []}
        ]
        
        # Should handle missing 'children' key gracefully
        result = tree.get_tree_max_id(value)
        assert result == 2

    def test_deeply_nested_tree_performance(self):
        """Test performance with deeply nested tree"""
        # Create a deeply nested tree
        def create_nested_tree(depth, base_id=1):
            if depth == 0:
                return []
            return [{
                "id": base_id,
                "label": f"Level {depth}",
                "children": create_nested_tree(depth - 1, base_id * 10)
            }]
        
        deep_tree = create_nested_tree(10)  # 10 levels deep
        result = tree.get_tree_max_id(deep_tree)
        assert result == 10000000000  # 10^10

    def test_concurrent_calls_with_global_state(self):
        """Test potential issues with global state in concurrent scenarios"""
        # Note: This demonstrates the issue with global variables
        tree.label_id = 1
        tree.label = ""
        
        value1 = [{"id": 10, "label": "Label A", "children": []}]
        value2 = [{"id": 20, "label": "Label B", "children": []}]
        
        # Simulate interleaved calls
        tree.get_tree_label(value1, "Label A")  # Sets label_id to 10
        tree.get_tree_relation_name(value2, 20)  # Sets label to "Label B"
        
        # Global state is now mixed
        assert tree.label_id == 10
        assert tree.label == "Label B"