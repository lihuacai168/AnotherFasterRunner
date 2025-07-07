#!/usr/bin/env python3
"""
Security test script to verify all eval() and exec() replacements work correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastrunner.utils.safe_json_parser import safe_json_loads, safe_literal_eval

def test_safe_json_loads():
    """Test safe_json_loads function"""
    print("Testing safe_json_loads...")
    
    # Test valid JSON
    assert safe_json_loads('{"key": "value"}') == {"key": "value"}
    assert safe_json_loads('[1, 2, 3]') == [1, 2, 3]
    assert safe_json_loads('null') is None
    assert safe_json_loads('true') is True
    assert safe_json_loads('123') == 123
    
    # Test Python dict/list strings
    assert safe_json_loads("{'key': 'value'}") == {"key": "value"}
    assert safe_json_loads("{'bool': True, 'none': None}") == {"bool": True, "none": None}
    
    # Test empty input
    assert safe_json_loads('') == {}
    assert safe_json_loads(None) == {}
    
    # Test already parsed objects
    assert safe_json_loads({"key": "value"}) == {"key": "value"}
    assert safe_json_loads([1, 2, 3]) == [1, 2, 3]
    
    print("✓ safe_json_loads tests passed")

def test_safe_literal_eval():
    """Test safe_literal_eval function"""
    print("\nTesting safe_literal_eval...")
    
    # Test valid literals
    assert safe_literal_eval("{'key': 'value'}") == {"key": "value"}
    assert safe_literal_eval("[1, 2, 3]") == [1, 2, 3]
    assert safe_literal_eval("(1, 2, 3)") == (1, 2, 3)
    assert safe_literal_eval("True") is True
    assert safe_literal_eval("123") == 123
    
    # Test empty input
    assert safe_literal_eval('') is None
    assert safe_literal_eval(None) is None
    
    # Test non-string input
    assert safe_literal_eval(123) == 123
    
    # Test unsafe expressions should fail
    try:
        safe_literal_eval("__import__('os').system('ls')")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ safe_literal_eval tests passed")

def test_security_fixes():
    """Test that dangerous eval/exec patterns are blocked"""
    print("\nTesting security fixes...")
    
    # Test that we can't execute dangerous code
    dangerous_inputs = [
        "__import__('os').system('echo hacked')",
        "eval('print(1+1)')",
        "exec('import os; os.system(\"ls\")')",
        "compile('print(1)', '<string>', 'exec')",
        "open('/etc/passwd', 'r').read()",
    ]
    
    for dangerous_input in dangerous_inputs:
        try:
            safe_literal_eval(dangerous_input)
            assert False, f"Should have blocked: {dangerous_input}"
        except ValueError:
            pass  # Expected
    
    print("✓ Security tests passed")

def main():
    """Run all tests"""
    print("Running security fix verification tests...\n")
    
    test_safe_json_loads()
    test_safe_literal_eval()
    test_security_fixes()
    
    print("\n✅ All security tests passed!")
    print("\nSummary of security fixes:")
    print("- Replaced eval() with safe_json_loads() for JSON data")
    print("- Replaced eval() with safe_literal_eval() for Python literals")
    print("- Added whitelist of allowed builtin functions in httprunner")
    print("- Added restricted execution environment for mock API code")
    print("- Created safe expression evaluator for comparisons")
    print("- SECRET_KEY now uses environment variable")

if __name__ == "__main__":
    main()