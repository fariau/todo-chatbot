from typing import Dict, Any, List
from ..core.llm_config import get_gemini_client, get_system_prompt, get_agent_config, get_available_tools
from ..mcp.tools import get_mcp_server
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from sqlmodel import Session
from ..core.database import get_session
import json


class TodoAgent:
    """
    Todo AI Agent that uses OpenAI's API to process natural language commands
    and interact with the Todo application through MCP tools.
    """

    def __init__(self):
        try:
            self.model = get_gemini_client()
            self.use_gemini = True
        except ValueError:
            # Fallback when Gemini API is not available
            self.model = None
            self.use_gemini = False

        self.system_prompt = get_system_prompt()
        self.agent_config = get_agent_config()
        self.tools = get_available_tools()

    def run(self, user_input: str, user_id: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent with user input and conversation history.

        Args:
            user_input: The user's message/command
            user_id: The user's ID for context and isolation
            conversation_history: List of previous messages in the conversation

        Returns:
            Dict containing response and any tool calls executed
        """

        # Check if we can use Gemini API
        if not self.use_gemini:
            # Fallback response when Gemini API is not available
            if "hello" in user_input.lower() or "hi" in user_input.lower() or "hey" in user_input.lower():
                response_text = "Hello! I'm your Todo AI assistant. Unfortunately, I'm currently unable to connect to the AI service. You can still manage your tasks manually through the UI."
            elif any(word in user_input.lower() for word in ["add", "create", "new", "task"]):
                response_text = "I understand you'd like to add a task. Unfortunately, I'm currently unable to connect to the AI service. You can still add tasks manually through the UI."
            elif any(word in user_input.lower() for word in ["list", "show", "see", "view"]):
                response_text = "I understand you'd like to see your tasks. Unfortunately, I'm currently unable to connect to the AI service. You can still view your tasks manually through the UI."
            else:
                response_text = "I'm currently unable to connect to the AI service. Please check the API configuration or try again later. You can still manage your tasks manually through the UI."

            return {
                "response": response_text,
                "tool_calls": []
            }

        try:
            # Prepare the chat history for Gemini
            chat_history = []

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"  # Gemini uses "model" instead of "assistant"
                    chat_history.append({
                        "role": role,
                        "parts": [msg["content"]]  # Gemini expects content directly, not wrapped in {"text": ...}
                    })

            # Start the chat with the history
            chat = self.model.start_chat(history=chat_history)

            # Prepare the tools for function calling
            from google.generativeai.types import FunctionDeclaration, Tool
            import json

            # Create function declarations for each tool
            function_declarations = []
            for tool in self.tools:
                func_decl = FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=tool["parameters"]
                )
                function_declarations.append(func_decl)

            # Create a tool with all function declarations
            tool_obj = Tool(function_declarations=function_declarations)

            # Generate content with the user input and tools
            response = chat.send_message(
                user_input,
                tools=[tool_obj],
                generation_config={
                    "temperature": self.agent_config["temperature"],
                    "max_output_tokens": self.agent_config.get("max_output_tokens", 1000)
                }
            )

            # Process the response
            tool_results = []

            # Check if the response contains function calls
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    # Check if this part has a function_call attribute AND it's not None
                    if (hasattr(part, 'function_call') and
                        part.function_call is not None and
                        hasattr(part.function_call, 'name') and
                        part.function_call.name):  # Check that the name is not empty

                        # Process function call
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = {}

                        # Extract function arguments - convert protobuf to dict properly
                        if hasattr(function_call, 'args') and function_call.args is not None:
                            # Convert the protobuf args to regular Python dict
                            function_args = {}
                            for key, value in function_call.args.items():
                                function_args[key] = value
                        else:
                            # If no args are provided, initialize as empty dict
                            function_args = {}

                        # Add user_id to function args if not present
                        if 'user_id' not in function_args:
                            function_args['user_id'] = user_id

                        # Execute the tool call
                        result = self._execute_tool(function_name, function_args)

                        tool_results.append({
                            "name": function_name,
                            "arguments": function_args,
                            "result": result
                        })

                        # For now, skip sending function result back to avoid the error
                        # This is a workaround for the current Gemini API issue
                        pass

            # Generate final response based on tool calls and text content
            if tool_results:
                # If there were tool calls, generate a natural response based on results
                final_response = self._generate_natural_response_from_tool_calls(tool_results)
            else:
                # If no tool calls, get the text response
                final_response = ""
                if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_response += part.text
                        elif isinstance(part, str):
                            final_response += part

                # If no text response was generated, provide a default
                if not final_response.strip():
                    final_response = "I've processed your request. Is there anything else I can help you with?"

            return {
                "response": final_response,
                "tool_calls": tool_results
            }

        except Exception as e:
            # Handle any errors in the agent execution
            error_msg = str(e)

            # Check for specific Gemini API errors
            if "quota" in error_msg.lower() or "exceeded" in error_msg.lower() or "429" in str(error_msg):
                # Provide a more helpful error message and potentially fallback behavior
                print(f"Gemini API Quota Error: {error_msg}")  # Log for debugging
                error_response = "I'm currently experiencing high demand and need a moment to process your request. This is a temporary issue with the AI service. Please try again in a few minutes."
            elif "rate_limit" in error_msg.lower() or "Too Many Requests" in error_msg:
                print(f"Gemini API Rate Limit Error: {error_msg}")  # Log for debugging
                error_response = "I'm currently experiencing high demand and need a moment to process your request. Please wait a few seconds and try again."
            elif "invalid" in error_msg.lower() or "auth" in error_msg.lower() or "api_key" in error_msg.lower():
                print(f"Gemini API Authentication Error: {error_msg}")  # Log for debugging
                error_response = "There seems to be an issue with my connection to the AI service. Please contact the administrator to check the API configuration."
            elif "Could not convert part.function_call to text" in error_msg:
                print(f"Gemini API Function Call Error: {error_msg}")  # Log for debugging
                error_response = "I had trouble processing your request. Could you please rephrase it? For example, instead of 'add task buy milk', you could say 'I want to add a task to buy milk'."
            elif "models/" in error_msg and "is not found" in error_msg:
                print(f"Gemini API Model Error: {error_msg}")  # Log for debugging
                error_response = "I'm having trouble connecting to the AI service. Please contact the administrator to check if the correct model is configured."
            else:
                print(f"Unexpected error in Gemini API: {error_msg}")  # Log for debugging
                error_response = f"I encountered an error processing your request: {str(e)}. Please try again."

            return {
                "response": error_response,
                "tool_calls": [],
                "error": str(e)
            }

    def _execute_tool(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool with the given arguments.

        Args:
            function_name: Name of the tool to execute
            function_args: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        # In a real implementation, we would connect to the MCP server to execute the tools
        # For now, we'll simulate the tool execution by directly calling the services

        # Import services here to avoid circular imports
        from ..services.todo_service import TaskService
        from ..services.conversation_service import ConversationService
        from ..services.message_service import MessageService
        from ..core.database import get_session
        from sqlmodel import Session

        # Get a session for the tool execution
        session_gen = get_session()
        session: Session = next(session_gen)

        try:
            if function_name == "add_task":
                # Execute add_task through the service
                task = TaskService.create_task(
                    session=session,
                    user_id=function_args.get('user_id'),
                    title=function_args.get('title'),
                    description=function_args.get('description')
                )

                return {
                    "task_id": task.id,
                    "status": "created",
                    "title": task.title
                }
            elif function_name == "list_tasks":
                # Execute list_tasks through the service
                status = function_args.get('status', 'all')
                tasks = TaskService.get_tasks(
                    session=session,
                    user_id=function_args.get('user_id'),
                    status=status
                )

                # Format tasks for response
                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else "",
                        "updated_at": task.updated_at.isoformat() if task.updated_at else ""
                    })

                return {
                    "tasks": task_list
                }
            elif function_name == "complete_task":
                # Execute complete_task through the service
                task = TaskService.complete_task(
                    session=session,
                    user_id=function_args.get('user_id'),
                    task_id=function_args.get('task_id')
                )

                return {
                    "status": "completed",
                    "task_id": task.id,
                    "title": task.title
                }
            elif function_name == "delete_task":
                # Execute delete_task through the service
                success = TaskService.delete_task(
                    session=session,
                    user_id=function_args.get('user_id'),
                    task_id=function_args.get('task_id')
                )

                # Get the task to return its title in the response
                task = TaskService.get_task_by_id(
                    session=session,
                    user_id=function_args.get('user_id'),
                    task_id=function_args.get('task_id')
                )

                return {
                    "status": "deleted",
                    "task_id": function_args.get('task_id'),
                    "title": task.title if task else "Unknown task"
                }
            elif function_name == "update_task":
                # Execute update_task through the service
                task = TaskService.update_task(
                    session=session,
                    user_id=function_args.get('user_id'),
                    task_id=function_args.get('task_id'),
                    title=function_args.get('title'),
                    description=function_args.get('description')
                )

                return {
                    "status": "updated",
                    "task_id": task.id,
                    "title": task.title
                }
            else:
                return {
                    "status": "error",
                    "message": f"Unknown tool: {function_name}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            session.close()

    def process_conversation(self, user_input: str, user_id: str, conversation_id: int = None) -> Dict[str, Any]:
        """
        Process a conversation with history management.

        Args:
            user_input: The user's message/command
            user_id: The user's ID for context and isolation
            conversation_id: Existing conversation ID or None to start new

        Returns:
            Dict containing response, conversation_id, and tool calls
        """
        # Get or create conversation
        with next(get_session()) as session:
            if conversation_id:
                # Get existing conversation
                conversation = ConversationService.get_conversation_by_id(
                    session, user_id, conversation_id
                )
                if not conversation:
                    # If conversation doesn't exist for user, create new one
                    conversation = ConversationService.create_conversation(session, user_id)
                    conversation_id = conversation.id
            else:
                # Create new conversation
                conversation = ConversationService.create_conversation(session, user_id)
                conversation_id = conversation.id

            # Save user message
            MessageService.create_message(
                session, user_id, conversation_id, "user", user_input
            )

            # Get conversation history
            messages = MessageService.get_messages_by_conversation(session, user_id, conversation_id)

            # Format history for agent
            conversation_history = []
            for msg in messages[:-1]:  # Exclude the current user message we just added
                conversation_history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Run the agent
            result = self.run(user_input, user_id, conversation_history)

            # Save assistant response
            MessageService.create_message(
                session, user_id, conversation_id, "assistant", result["response"]
            )

            # Update conversation timestamp
            ConversationService.update_conversation(session, user_id, conversation_id)

        return {
            "conversation_id": conversation_id,
            "response": result["response"],
            "tool_calls": result["tool_calls"]
        }

    def _generate_natural_response_from_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> str:
        """
        Generate a natural, conversational response based on tool execution results
        """
        if not tool_calls:
            return "I've processed your request. Is there anything else I can help you with?"

        responses = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name", "")
            result = tool_call.get("result", {})
            args = tool_call.get("arguments", {})

            if tool_name == "add_task":
                status = result.get("status", "unknown")
                if status == "created":
                    task_title = args.get("title", "unknown task")
                    responses.append(f"I've added the task '{task_title}' for you!")
                else:
                    error_msg = result.get("message", "Unknown error")
                    responses.append(f"I couldn't add that task. {error_msg}")

            elif tool_name == "list_tasks":
                tasks = result.get("tasks", [])
                if tasks:
                    task_titles = [task.get('title', 'unknown') for task in tasks]
                    if len(task_titles) == 1:
                        responses.append(f"Here is your task: {task_titles[0]}")
                    else:
                        task_list = ", ".join(task_titles)
                        responses.append(f"Here are your tasks: {task_list}")
                else:
                    responses.append("You don't have any tasks at the moment.")

            elif tool_name == "complete_task":
                status = result.get("status", "unknown")
                if status == "completed":
                    responses.append("I've marked that task as completed!")
                else:
                    error_msg = result.get("message", "Unknown error")
                    responses.append(f"I couldn't complete that task. {error_msg}")

            elif tool_name == "delete_task":
                status = result.get("status", "unknown")
                if status == "deleted":
                    responses.append("I've deleted that task for you.")
                else:
                    error_msg = result.get("message", "Unknown error")
                    responses.append(f"I couldn't delete that task. {error_msg}")

            elif tool_name == "update_task":
                status = result.get("status", "unknown")
                if status == "updated":
                    responses.append("I've updated that task for you.")
                else:
                    error_msg = result.get("message", "Unknown error")
                    responses.append(f"I couldn't update that task. {error_msg}")

            else:
                responses.append("I've processed your request.")

        return " ".join(responses)