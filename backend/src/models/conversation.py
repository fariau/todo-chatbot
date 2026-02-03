from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ConversationBase(SQLModel):
    """Base class for Conversation model with common fields"""
    user_id: str = Field(index=True)                   # Unique identifier for the user (indexed)


class Conversation(ConversationBase, table=True):
    """Conversation model representing a user's conversation thread"""
    __tablename__ = "conversations"
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the conversation
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of creation (indexed)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of last update (indexed)

    # Constraints: user_id must be valid string, id is auto-generated