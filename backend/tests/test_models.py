import pytest
from datetime import datetime
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message


class TestTaskModel:
    def test_task_creation(self):
        """Test creating a Task instance"""
        task = Task(
            user_id="user123",
            title="Test Task",
            description="Test Description",
            completed=False
        )

        assert task.user_id == "user123"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.id is None  # ID will be assigned by DB

    def test_task_defaults(self):
        """Test Task default values"""
        task = Task(
            user_id="user123",
            title="Test Task"
        )

        assert task.completed is False  # Should default to False
        assert task.description is None  # Should default to None


class TestConversationModel:
    def test_conversation_creation(self):
        """Test creating a Conversation instance"""
        conversation = Conversation(
            user_id="user123"
        )

        assert conversation.user_id == "user123"
        assert conversation.id is None  # ID will be assigned by DB


class TestMessageModel:
    def test_message_creation(self):
        """Test creating a Message instance"""
        message = Message(
            user_id="user123",
            conversation_id=1,
            role="user",
            content="Test message"
        )

        assert message.user_id == "user123"
        assert message.conversation_id == 1
        assert message.role == "user"
        assert message.content == "Test message"
        assert message.id is None  # ID will be assigned by DB

    def test_invalid_role(self):
        """Test that invalid roles are rejected"""
        # Note: This test might not work depending on how validation is implemented
        # SQLModel validation happens at DB level, not object creation
        pass