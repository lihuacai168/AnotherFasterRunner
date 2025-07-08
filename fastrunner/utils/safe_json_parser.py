"""
Safe JSON parser utility to replace eval() usage for security.
"""
import ast
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
    
    # First try standard JSON parsing
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        pass
    
    # If JSON parsing fails, try ast.literal_eval for Python literals
    try:
        result = ast.literal_eval(data)
        # Ensure the result is JSON-serializable
        if isinstance(result, (dict, list, str, int, float, bool, type(None))):
            return result
        else:
            # Convert tuples to lists for JSON compatibility
            if isinstance(result, tuple):
                return list(result)
            # Convert sets to lists
            elif isinstance(result, set):
                return list(result)
            else:
                raise ValueError(f"Unsupported type: {type(result)}")
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid data format: {e}")


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