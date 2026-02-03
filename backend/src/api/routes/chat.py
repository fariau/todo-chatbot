from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlmodel import Session
from ...core.database import get_session
from ...agents.todo_agent import TodoAgent
from ...services.message_service import MessageService
from ...services.conversation_service import ConversationService

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ToolCallResult(BaseModel):
    name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCallResult]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str = Path(..., description="User ID"),
    chat_request: ChatRequest = None,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that processes user messages through the AI agent.

    Args:
        user_id: The user's ID
        chat_request: Contains conversation_id (optional) and message
        session: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool calls
    """
    if not chat_request or not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Initialize the agent
        agent = TodoAgent()

        # Process the conversation (handles history, message saving, agent running, response saving)
        result = agent.process_conversation(
            user_input=chat_request.message,
            user_id=user_id,
            conversation_id=chat_request.conversation_id
        )

        # Convert tool calls to the expected format
        formatted_tool_calls = [
            ToolCallResult(
                name=call["name"],
                arguments=call["arguments"],
                result=call["result"]
            )
            for call in result["tool_calls"]
        ]

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=formatted_tool_calls
        )

    except Exception as e:
        error_msg = str(e)

        # Check for specific OpenAI API errors and provide user-friendly messages
        if "insufficient_quota" in error_msg.lower() or "429" in error_msg:
            detail = "I apologize, but I've reached my usage limit for now. This happens when the AI service has exceeded its quota. Please try again later or contact the administrator to check the API plan and billing details."
        elif "rate_limit_exceeded" in error_msg.lower() or "Too Many Requests" in error_msg:
            detail = "I'm currently experiencing high demand and need a moment to process your request. Please wait a few seconds and try again."
        elif "invalid_api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            detail = "There seems to be an issue with my connection to the AI service. Please contact the administrator to check the API configuration."
        else:
            detail = f"I encountered an error processing your request. Please try again."

        raise HTTPException(status_code=500, detail=detail)