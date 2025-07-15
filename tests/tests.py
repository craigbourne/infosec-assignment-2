"""
Simple tests to validate attack tree calculations.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from attack_tree import AttackTree


def test_or_gate_logic():
    """Test OR gate takes maximum value."""
    tree = AttackTree()
    
    # Create simple test data
    test_data = {
        "name": "Test OR Gate",
        "root": {
            "id": "root",
            "name": "Test OR",
            "type": "OR",
            "children": [
                {"id": "leaf1", "name": "Attack 1", "type": "leaf", "value": 100},
                {"id": "leaf2", "name": "Attack 2", "type": "leaf", "value": 200}
            ]
        }
    }
    
    tree.tree_data = test_data
    tree.build_graph()
    
    # OR gate should return maximum (200)
    result = tree._calculate_node_risk("root")
    assert result == 200, f"Expected 200, got {result}"
    print("✓ OR gate test passed")


def test_and_gate_logic():
    """Test AND gate sums all values."""
    tree = AttackTree()
    
    test_data = {
        "name": "Test AND Gate", 
        "root": {
            "id": "root",
            "name": "Test AND",
            "type": "AND",
            "children": [
                {"id": "leaf1", "name": "Step 1", "type": "leaf", "value": 100},
                {"id": "leaf2", "name": "Step 2", "type": "leaf", "value": 200}
            ]
        }
    }
    
    tree.tree_data = test_data
    tree.build_graph()
    
    # AND gate should return sum (300)
    result = tree._calculate_node_risk("root")
    assert result == 300, f"Expected 300, got {result}"
    print("✓ AND gate test passed")


if __name__ == "__main__":
    print("Running attack tree calculation tests...")
    test_or_gate_logic()
    test_and_gate_logic()
    print("✓ All tests passed!")