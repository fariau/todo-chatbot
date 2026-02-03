#!/usr/bin/env python3
"""
Script to list available Gemini models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("GEMINI_API_KEY environment variable is not set")
    exit(1)

# Configure the API
genai.configure(api_key=api_key)

# List all available models
print("Available Gemini models:")
try:
    for model in genai.list_models():
        print(f"- {model.name}")
        # Check if the model supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            print(f"  Supports generateContent: Yes")
        else:
            print(f"  Supports generateContent: No")
        print(f"  Description: {model.description}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")