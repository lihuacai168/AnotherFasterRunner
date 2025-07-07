"""
Safe JSON parser utility to replace eval() usage for security.
"""
import json
from typing import Any, Dict, List, Union


def safe_json_loads(data: str) -> Union[Dict, List, Any]:
    """
    Safely parse JSON string to Python object.
    
    Args:
        data: JSON string to parse
        
    Returns:
        Parsed Python object (dict, list, etc.)
        
    Raises:
        ValueError: If data is not valid JSON
    """
    if not data:
        return {}
    
    if isinstance(data, (dict, list)):
        return data
        
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        # Try to handle Python dict/list strings by converting quotes
        try:
            # Replace single quotes with double quotes for JSON compatibility
            json_str = data.replace("'", '"').replace('True', 'true').replace('False', 'false').replace('None', 'null')
            return json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON data: {e}")


def safe_literal_eval(data: str) -> Any:
    """
    Safely evaluate a string containing a Python literal.
    Uses ast.literal_eval which is safe for untrusted data.
    
    Args:
        data: String containing Python literal
        
    Returns:
        Evaluated Python object
        
    Raises:
        ValueError: If data contains unsafe expressions
    """
    import ast
    
    if not data:
        return None
        
    if not isinstance(data, str):
        return data
        
    try:
        return ast.literal_eval(data)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal: {e}")