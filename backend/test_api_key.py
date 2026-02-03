#!/usr/bin/env python3
"""
Test script to verify the new API key is working properly
"""

import os
from dotenv import load_dotenv
from src.core.llm_config import get_gemini_client

def test_api_key():
    """Test if the API key works with a simple call"""

    # Load environment variables
    load_dotenv()

    print("Testing API key with Gemini client...")

    try:
        # Get the client
        model = get_gemini_client()
        print(f"[OK] Client created successfully with model: {model.model_name}")

        # Test a simple message without tools to isolate the issue
        print("Testing simple text generation without tools...")

        response = model.generate_content(
            "Say 'Hello' in a friendly way",
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 100
            }
        )

        print(f"[OK] Response received: {response.text}")
        print("[OK] API key is working correctly!")
        return True

    except Exception as e:
        print(f"[ERROR] Error with API key: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_api_key()