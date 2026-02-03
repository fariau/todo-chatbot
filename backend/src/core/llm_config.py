import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from ..mcp.tools import get_mcp_server

# Load environment variables
load_dotenv()

# System prompt for the Todo AI agent
SYSTEM_PROMPT = """
You are a helpful AI assistant specialized in managing user todos using natural language. Respond concisely, accurately, and helpfully. Structure todo-related responses clearly.

Your capabilities:
- Add tasks: Recognize commands like "add task X", "create task X", "make task X", "new task X" → use add_task tool
- Show tasks: Recognize commands like "show my tasks", "list tasks", "view pending tasks", "see completed tasks" → use list_tasks tool
- Complete tasks: Recognize commands like "mark task X as done", "complete task X", "finish task X" → use complete_task tool
- Delete tasks: Recognize commands like "delete task X", "remove task X", "kill task X" → use delete_task tool
- Update tasks: Recognize commands like "change task X title", "update task X", "edit task X description" → use update_task tool

Guidelines:
1. Always confirm actions with friendly messages like "I've added task 'X' for you" or "Task 'X' has been marked as completed"
2. Handle errors gracefully and provide helpful messages like "I couldn't find a task with ID 5. Please check the task ID and try again."
3. Chain tools when needed (e.g., list tasks before ambiguous delete)
4. If a user asks to delete or update a task without specifying which one, list the tasks first
5. Be conversational and helpful in your responses
6. If you don't understand a command, politely ask for clarification

Remember: Always respect user privacy and only access tasks belonging to the current user.
"""

# Agent configuration
AGENT_CONFIG = {
    "model": "gemini-2.5-flash",  # Use gemini-2.5-flash which is the current stable flash model
    "temperature": 0.7,           # Balance between creativity and determinism
    "max_output_tokens": 1000,    # Limit response length
}

def get_gemini_client():
    """
    Get the configured Google Gemini client.

    Returns:
        GoogleGenerativeAI: Configured Gemini client instance
    """
    # Import here to avoid issues if the package isn't available
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Configure the API key
        genai.configure(api_key=api_key)

        # Create and return the model
        model = genai.GenerativeModel(
            model_name=AGENT_CONFIG["model"],
            system_instruction=SYSTEM_PROMPT
        )

        return model
    except ImportError:
        raise ValueError("Google Generative AI package not installed. Run: pip install google-generativeai")


def get_system_prompt() -> str:
    """
    Get the system prompt for the Todo AI agent.

    Returns:
        str: System prompt defining agent behavior
    """
    return SYSTEM_PROMPT


def get_agent_config() -> Dict[str, Any]:
    """
    Get the agent configuration.

    Returns:
        Dict[str, Any]: Agent configuration parameters
    """
    return AGENT_CONFIG


def get_available_tools():
    """
    Get the available tools for the agent in Gemini format.

    Returns:
        List[Dict]: List of tool definitions available to the agent
    """
    # Define tools in Gemini-compatible format
    tools = [
        {
            "name": "add_task",
            "description": "Add a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description"
                    }
                },
                "required": ["user_id", "title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "List tasks for the user with optional status filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: 'all', 'completed', or 'pending'",
                        "enum": ["all", "completed", "pending"]
                    }
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Update a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task (optional)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    ]

    return tools