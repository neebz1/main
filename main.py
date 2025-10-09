#!/usr/bin/env python3
"""
Main application - A simple working program
"""


def greet(name="World"):
    """
    Return a greeting message.
    
    Args:
        name (str): Name to greet. Defaults to "World".
    
    Returns:
        str: Greeting message
    """
    return f"Hello, {name}!"


def main():
    """Main entry point of the application."""
    message = greet()
    print(message)
    return 0


if __name__ == "__main__":
    exit(main())
