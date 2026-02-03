#!/usr/bin/env python3
"""
Debug script to examine Gemini API responses
"""

import os
from dotenv import load_dotenv
from src.core.llm_config import get_gemini_client, get_available_tools
from google.generativeai.types import FunctionDeclaration, Tool

def debug_gemini():
    """Debug the Gemini response to see what's happening with function calls"""

    # Load environment variables
    load_dotenv()

    # Get the client
    model = get_gemini_client()

    # Get the available tools
    tools = get_available_tools()
    print("Available tools:", tools)

    # Create function declarations
    function_declarations = []
    for tool in tools:
        func_decl = FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters=tool["parameters"]
        )
        function_declarations.append(func_decl)

    # Create a tool with all function declarations
    tool_obj = Tool(function_declarations=function_declarations)

    print("\nFunction declarations created:", [fd.name for fd in function_declarations])

    # Start chat without history
    chat = model.start_chat()

    # Send a test message
    user_input = "Say hello"
    print(f"\nSending message: {user_input}")

    try:
        response = chat.send_message(
            user_input,
            tools=[tool_obj],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000
            }
        )

        print(f"\nResponse received: {response}")
        print(f"Response text: {getattr(response, 'text', 'No text')}")

        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            print(f"Candidate: {candidate}")

            if hasattr(candidate, 'content') and candidate.content:
                content = candidate.content
                print(f"Content: {content}")

                if hasattr(content, 'parts') and content.parts:
                    print(f"Parts: {content.parts}")
                    for i, part in enumerate(content.parts):
                        print(f"Part {i}: {part} (type: {type(part)})")

                        if hasattr(part, 'function_call'):
                            print(f"  -> Function call detected: {part.function_call}")
                            if hasattr(part.function_call, 'name'):
                                print(f"     Function name: '{part.function_call.name}'")
                            if hasattr(part.function_call, 'args'):
                                print(f"     Function args: {part.function_call.args}")

    except Exception as e:
        print(f"Error during API call: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_gemini()