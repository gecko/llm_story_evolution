#!/usr/bin/env python3
"""
Simple test script for LLM Fixpoints Explorer.
This script provides a basic way to test the application without user interaction.
"""

from app import Application

def main():
    """Run a simple test of the application."""
    print("Running LLM Fixpoints Explorer test...")

    # Create a mock input function to avoid user interaction
    original_input = __builtins__.input

    def mock_input(prompt):
        if "Enter a name for your story" in prompt:
            return "Test Story"
        elif "Title" in prompt:
            return "A Journey Through Time"
        elif "Main characters" in prompt:
            return "Alice, Bob"
        elif "Setting" in prompt:
            return "A futuristic city"
        elif "Plot points" in prompt:
            return "Time travel, adventure, discovery"
        elif "Theme" in prompt:
            return "The power of friendship"
        elif "How many times should the story be retold" in prompt:
            return "3"
        return ""

    # Replace the input function
    __builtins__.input = mock_input

    try:
        app = Application()
        app.run()
    finally:
        # Restore the original input function
        __builtins__.input = original_input

if __name__ == "__main__":
    main()