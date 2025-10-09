#!/usr/bin/env python3
"""
Tests for main.py
"""

import unittest
from main import greet, main


class TestMain(unittest.TestCase):
    """Test cases for main application."""
    
    def test_greet_default(self):
        """Test greet function with default parameter."""
        result = greet()
        self.assertEqual(result, "Hello, World!")
    
    def test_greet_custom_name(self):
        """Test greet function with custom name."""
        result = greet("Alice")
        self.assertEqual(result, "Hello, Alice!")
    
    def test_main_returns_zero(self):
        """Test that main function returns 0."""
        result = main()
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
