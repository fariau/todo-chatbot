from sqlmodel import Session, select
from typing import List, Optional
from ..models.message import Message

# Define custom exceptions
class MessageNotFoundError(Exception):
    """Raised when a message is not found for a given user"""
    def __init__(self, user_id: str, message_id: int):
        self.user_id = user_id
        self.message_id = message_id
        super().__init__(f"Message with ID {message_id} not found for user {user_id}")


class MessageService:
    """Service class for managing messages"""

    @staticmethod
    def create_message(session: Session, user_id: str, conversation_id: int, role: str, content: str) -> Message:
        """
        Create a new message for the user in a conversation.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Conversation ID
            role: Message role ("user" or "assistant")
            content: Message content

        Returns:
            Created Message object

        Raises:
            ValueError: If role is not "user" or "assistant", or content is empty
        """
        if role not in ["user", "assistant"]:
            raise ValueError(f"Role must be 'user' or 'assistant', got '{role}'")

        if not content.strip():
            raise ValueError("Message content cannot be empty")

        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content.strip()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_message_by_id(session: Session, user_id: str, message_id: int) -> Optional[Message]:
        """
        Get a specific message by ID for the user.

        Args:
            session: Database session
            user_id: User identifier
            message_id: Message ID

        Returns:
            Message object if found, None otherwise
        """
        query = select(Message).where(
            Message.user_id == user_id,
            Message.id == message_id
        )
        return session.exec(query).first()

    @staticmethod
    def get_messages_by_conversation(session: Session, user_id: str, conversation_id: int) -> List[Message]:
        """
        Get all messages for a specific conversation and user.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Conversation ID

        Returns:
            List of Message objects
        """
        query = select(Message).where(
            Message.user_id == user_id,
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        return session.exec(query).all()

    @staticmethod
    def get_messages(session: Session, user_id: str) -> List[Message]:
        """
        Get all messages for a user.

        Args:
            session: Database session
            user_id: User identifier

        Returns:
            List of Message objects
        """
        query = select(Message).where(Message.user_id == user_id).order_by(Message.created_at)
        return session.exec(query).all()

    @staticmethod
    def update_message(session: Session, user_id: str, message_id: int, content: Optional[str] = None) -> Message:
        """
        Update a message for the user.

        Args:
            session: Database session
            user_id: User identifier
            message_id: Message ID to update
            content: New content (optional)

        Returns:
            Updated Message object

        Raises:
            MessageNotFoundError: If message doesn't exist for user
        """
        message = MessageService.get_message_by_id(session, user_id, message_id)
        if not message:
            raise MessageNotFoundError(user_id, message_id)

        # Update fields if provided
        if content is not None:
            if not content.strip():
                raise ValueError("Message content cannot be empty")
            message.content = content.strip()

        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def delete_message(session: Session, user_id: str, message_id: int) -> bool:
        """
        Delete a message for the user.

        Args:
            session: Database session
            user_id: User identifier
            message_id: Message ID to delete

        Returns:
            True if message was deleted, False if not found

        Raises:
            MessageNotFoundError: If message doesn't exist for user
        """
        message = MessageService.get_message_by_id(session, user_id, message_id)
        if not message:
            raise MessageNotFoundError(user_id, message_id)

        session.delete(message)
        session.commit()
        return True