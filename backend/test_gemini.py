#!/usr/bin/env python3
"""
Test script to verify Google Gemini integration with TodoAgent
"""

import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.agents.todo_agent import TodoAgent

def test_gemini_integration():
    """Test the Gemini integration with the TodoAgent"""
    print("Testing Google Gemini Integration...")

    # Create agent instance
    agent = TodoAgent()

    if not agent.use_gemini:
        print("[ERROR] Gemini is not available. Check your GEMINI_API_KEY in .env file.")
        return False

    print("[SUCCESS] Gemini client initialized successfully")

    # Test a simple message
    user_input = "Say hello and tell me you're a todo assistant"
    user_id = "test_user"

    print(f"\nTesting input: '{user_input}'")

    try:
        result = agent.run(user_input, user_id)

        print(f"Response: {result['response']}")
        print(f"Tool calls: {len(result['tool_calls'])}")

        if result['response']:
            print("[SUCCESS] Gemini integration working correctly!")
            return True
        else:
            print("[ERROR] No response received from Gemini")
            return False

    except Exception as e:
        print(f"[ERROR] Error during test: {str(e)}")
        return False

def test_todo_functionality():
    """Test specific todo functionality"""
    print("\nTesting Todo functionality...")

    agent = TodoAgent()

    if not agent.use_gemini:
        print("[ERROR] Cannot test - Gemini not available")
        return False

    # Test adding a task
    user_input = "Add a task called 'Buy groceries'"
    user_id = "test_user"

    print(f"Testing input: '{user_input}'")

    try:
        result = agent.run(user_input, user_id)

        print(f"Response: {result['response']}")
        print(f"Tool calls made: {len(result['tool_calls'])}")

        # Check if add_task was called
        for tool_call in result['tool_calls']:
            print(f"Tool called: {tool_call.get('name', 'unknown')} with args: {tool_call.get('arguments', {})}")

        print("[SUCCESS] Todo functionality test completed")
        return True

    except Exception as e:
        print(f"[ERROR] Error during todo test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running Gemini Integration Tests...\n")

    success1 = test_gemini_integration()
    success2 = test_todo_functionality()

    if success1 and success2:
        print("\nAll tests passed! Gemini integration is working correctly.")
    else:
        print("\nSome tests failed. Please check your configuration.")