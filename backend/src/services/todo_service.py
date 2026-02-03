from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task

# Define custom exceptions
class TaskNotFoundError(Exception):
    """Raised when a task is not found for a given user"""
    def __init__(self, user_id: str, task_id: int):
        self.user_id = user_id
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found for user {user_id}")


class TaskService:
    """Service class for managing tasks"""

    @staticmethod
    def create_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task for the user.

        Args:
            session: Database session
            user_id: User identifier
            title: Task title
            description: Optional task description

        Returns:
            Created Task object

        Raises:
            ValueError: If title is empty
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks(session: Session, user_id: str, status: str = "all") -> List[Task]:
        """
        Get tasks for a user with optional status filtering.

        Args:
            session: Database session
            user_id: User identifier
            status: Filter status ("all", "completed", "pending")

        Returns:
            List of Task objects
        """
        query = select(Task).where(Task.user_id == user_id)

        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
        elif status != "all":
            # Invalid status, default to all
            pass

        return session.exec(query).all()

    @staticmethod
    def get_task_by_id(session: Session, user_id: str, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID for the user.

        Args:
            session: Database session
            user_id: User identifier
            task_id: Task ID

        Returns:
            Task object if found, None otherwise
        """
        query = select(Task).where(Task.user_id == user_id, Task.id == task_id)
        return session.exec(query).first()

    @staticmethod
    def update_task(session: Session, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update a task for the user.

        Args:
            session: Database session
            user_id: User identifier
            task_id: Task ID to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist for user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if not task:
            raise TaskNotFoundError(user_id, task_id)

        # Update fields if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()
        if description is not None:
            task.description = description

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def complete_task(session: Session, user_id: str, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            session: Database session
            user_id: User identifier
            task_id: Task ID to complete

        Returns:
            Completed Task object

        Raises:
            TaskNotFoundError: If task doesn't exist for user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if not task:
            raise TaskNotFoundError(user_id, task_id)

        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: int) -> bool:
        """
        Delete a task for the user.

        Args:
            session: Database session
            user_id: User identifier
            task_id: Task ID to delete

        Returns:
            True if task was deleted, False if not found

        Raises:
            TaskNotFoundError: If task doesn't exist for user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if not task:
            raise TaskNotFoundError(user_id, task_id)

        session.delete(task)
        session.commit()
        return True