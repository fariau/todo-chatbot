from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class MessageBase(SQLModel):
    """Base class for Message model with common fields"""
    user_id: str = Field(index=True)                   # Unique identifier for the user (indexed)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)  # Foreign key to conversation (indexed) - using table name
    role: str = Field(regex="^(user|assistant)$", index=True)      # Message role (must be "user" or "assistant", indexed)
    content: str                                       # Message content (non-null)


class Message(MessageBase, table=True):
    """Message model representing a message in a conversation"""
    __tablename__ = "messages"
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the message
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of creation (indexed)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of last update (indexed)

    # Constraints: role must be "user" or "assistant", content must be non-empty