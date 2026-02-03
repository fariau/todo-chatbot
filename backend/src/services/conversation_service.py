from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation import Conversation

# Define custom exceptions
class ConversationNotFoundError(Exception):
    """Raised when a conversation is not found for a given user"""
    def __init__(self, user_id: str, conversation_id: int):
        self.user_id = user_id
        self.conversation_id = conversation_id
        super().__init__(f"Conversation with ID {conversation_id} not found for user {user_id}")


class ConversationService:
    """Service class for managing conversations"""

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Create a new conversation for the user.

        Args:
            session: Database session
            user_id: User identifier

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, user_id: str, conversation_id: int) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for the user.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Conversation ID

        Returns:
            Conversation object if found, None otherwise
        """
        query = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.id == conversation_id
        )
        return session.exec(query).first()

    @staticmethod
    def get_conversations(session: Session, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            session: Database session
            user_id: User identifier

        Returns:
            List of Conversation objects
        """
        query = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(query).all()

    @staticmethod
    def update_conversation(session: Session, user_id: str, conversation_id: int) -> Conversation:
        """
        Update a conversation's updated_at timestamp.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Conversation ID to update

        Returns:
            Updated Conversation object

        Raises:
            ConversationNotFoundError: If conversation doesn't exist for user
        """
        conversation = ConversationService.get_conversation_by_id(session, user_id, conversation_id)
        if not conversation:
            raise ConversationNotFoundError(user_id, conversation_id)

        # Just update the timestamp
        conversation.updated_at = conversation.updated_at  # This will trigger the default_factory

        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def delete_conversation(session: Session, user_id: str, conversation_id: int) -> bool:
        """
        Delete a conversation for the user.

        Args:
            session: Database session
            user_id: User identifier
            conversation_id: Conversation ID to delete

        Returns:
            True if conversation was deleted, False if not found

        Raises:
            ConversationNotFoundError: If conversation doesn't exist for user
        """
        conversation = ConversationService.get_conversation_by_id(session, user_id, conversation_id)
        if not conversation:
            raise ConversationNotFoundError(user_id, conversation_id)

        session.delete(conversation)
        session.commit()
        return True