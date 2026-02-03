from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    """Base class for Task model with common fields"""
    user_id: str = Field(index=True)                    # Unique identifier for the user (indexed)
    title: str                                         # Task title (non-null)
    description: Optional[str] = None                  # Optional task description
    completed: bool = Field(default=False, index=True) # Completion status (default: False, indexed for queries)


class Task(TaskBase, table=True):
    """Task model representing a user's todo item"""
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the task
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of creation (indexed)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)  # Timestamp of last update (indexed)

    # Constraints: user_id and title must be valid strings, id is auto-generated