import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from src.services.todo_service import TaskService, TaskNotFoundError
from src.models.task import Task


class TestTaskService:
    def setup_method(self):
        """Setup method run before each test"""
        self.session = MagicMock(spec=Session)

    def test_create_task_success(self):
        """Test successful task creation"""
        # Arrange
        user_id = "user123"
        title = "Test Task"
        description = "Test Description"

        # Mock task object to return
        mock_task = Task(
            id=1,
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )

        # Act
        with patch.object(self.session, 'add'), \
             patch.object(self.session, 'commit'), \
             patch.object(self.session, 'refresh', side_effect=lambda x: setattr(x, 'id', 1)):

            result = TaskService.create_task(
                session=self.session,
                user_id=user_id,
                title=title,
                description=description
            )

        # Assert
        assert result.user_id == user_id
        assert result.title == title
        assert result.description == description
        assert result.completed is False

    def test_create_task_empty_title(self):
        """Test that creating a task with empty title raises ValueError"""
        # Act & Assert
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            TaskService.create_task(
                session=self.session,
                user_id="user123",
                title="",
                description="Test"
            )

    def test_get_tasks(self):
        """Test getting tasks for a user"""
        # Arrange
        user_id = "user123"
        mock_tasks = [
            Task(id=1, user_id=user_id, title="Task 1", completed=False),
            Task(id=2, user_id=user_id, title="Task 2", completed=True)
        ]

        # Act
        with patch.object(self.session, 'exec', return_value=mock_tasks):
            result = TaskService.get_tasks(
                session=self.session,
                user_id=user_id
            )

        # Assert
        assert len(result) == 2
        assert result[0].title == "Task 1"
        assert result[1].title == "Task 2"

    def test_get_task_by_id_found(self):
        """Test getting a task by ID when it exists"""
        # Arrange
        user_id = "user123"
        task_id = 1
        mock_task = Task(id=task_id, user_id=user_id, title="Test Task", completed=False)

        # Act
        with patch.object(self.session, 'exec', return_value=MagicMock(first=lambda: mock_task)):
            result = TaskService.get_task_by_id(
                session=self.session,
                user_id=user_id,
                task_id=task_id
            )

        # Assert
        assert result is not None
        assert result.id == task_id
        assert result.title == "Test Task"

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID when it doesn't exist"""
        # Arrange
        user_id = "user123"
        task_id = 999

        # Act
        with patch.object(self.session, 'exec', return_value=MagicMock(first=lambda: None)):
            result = TaskService.get_task_by_id(
                session=self.session,
                user_id=user_id,
                task_id=task_id
            )

        # Assert
        assert result is None

    def test_complete_task_success(self):
        """Test successfully completing a task"""
        # Arrange
        user_id = "user123"
        task_id = 1
        mock_task = Task(id=task_id, user_id=user_id, title="Test Task", completed=False)

        # Act
        with patch.object(self.session, 'exec', return_value=MagicMock(first=lambda: mock_task)), \
             patch.object(self.session, 'add'), \
             patch.object(self.session, 'commit'), \
             patch.object(self.session, 'refresh'):

            result = TaskService.complete_task(
                session=self.session,
                user_id=user_id,
                task_id=task_id
            )

        # Assert
        assert result.completed is True
        assert result.title == "Test Task"

    def test_complete_task_not_found(self):
        """Test completing a task that doesn't exist"""
        # Arrange
        user_id = "user123"
        task_id = 999

        # Act & Assert
        with patch.object(self.session, 'exec', return_value=MagicMock(first=lambda: None)):
            with pytest.raises(TaskNotFoundError):
                TaskService.complete_task(
                    session=self.session,
                    user_id=user_id,
                    task_id=task_id
                )