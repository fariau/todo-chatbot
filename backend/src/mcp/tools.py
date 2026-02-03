import logging
from mcp import server, types
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlmodel import Session
from ..core.database import get_session
from ..services.todo_service import TaskService, TaskNotFoundError
from ..models.task import Task
from contextlib import contextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class AddTaskResponse(BaseModel):
    task_id: int
    status: str
    title: str


class ListTasksRequest(BaseModel):
    user_id: str
    status: Optional[str] = "all"


class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str


class ListTasksResponse(BaseModel):
    tasks: List[TaskResponse]


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class CompleteTaskResponse(BaseModel):
    status: str
    task_id: int
    title: str


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class DeleteTaskResponse(BaseModel):
    status: str
    task_id: int
    title: str


class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class UpdateTaskResponse(BaseModel):
    status: str
    task_id: int
    title: str


# Create MCP server instance
mcp_server = server.Server("todo-ai-mcp")


def validate_user_id(user_id: str) -> None:
    """Validate that user_id is not empty"""
    if not user_id or not user_id.strip():
        raise ValueError("user_id cannot be empty")


@contextmanager
def get_db_session():
    """Context manager to get database session"""
    session_gen = get_session()
    session: Session = next(session_gen)
    try:
        yield session
    finally:
        session.close()


@mcp_server.call_tool()
async def add_task_tool(request: AddTaskRequest) -> AddTaskResponse:
    """
    Add a new task for the user.

    Args:
        request: Contains user_id, title, and optional description

    Returns:
        AddTaskResponse with task_id, status, and title
    """
    # Validate inputs
    validate_user_id(request.user_id)
    if not request.title or not request.title.strip():
        raise ValueError("Task title cannot be empty")

    with get_db_session() as session:
        try:
            task = TaskService.create_task(
                session=session,
                user_id=request.user_id,
                title=request.title,
                description=request.description
            )

            logger.info(f"Task created successfully: ID {task.id} for user {request.user_id}")
            return AddTaskResponse(
                task_id=task.id,
                status="created",
                title=task.title
            )
        except ValueError as e:
            # Propagate ValueError as MCP-friendly error
            logger.error(f"ValueError in add_task: {str(e)}")
            raise e
        except Exception as e:
            # Handle any other exceptions that might occur
            logger.error(f"Unexpected error in add_task: {str(e)}")
            raise RuntimeError(f"Failed to create task: {str(e)}")


@mcp_server.call_tool()
async def list_tasks_tool(request: ListTasksRequest) -> ListTasksResponse:
    """
    List tasks for the user with optional status filtering.

    Args:
        request: Contains user_id and optional status filter ("all", "completed", "pending")

    Returns:
        ListTasksResponse with list of tasks
    """
    # Validate inputs
    validate_user_id(request.user_id)

    # Validate status parameter - default to "all" if not provided or invalid
    status = request.status
    if not status or status not in ["all", "completed", "pending"]:
        status = "all"

    with get_db_session() as session:
        try:
            tasks = TaskService.get_tasks(
                session=session,
                user_id=request.user_id,
                status=status
            )

            task_responses = []
            for task in tasks:
                task_responses.append(TaskResponse(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at.isoformat() if task.created_at else "",
                    updated_at=task.updated_at.isoformat() if task.updated_at else ""
                ))

            # Add structured logging for the number of tasks returned
            logger.info(f"Returning {len(task_responses)} tasks for user {request.user_id} with status filter '{status}'")

            return ListTasksResponse(tasks=task_responses)
        except Exception as e:
            # Handle any exceptions that might occur during task retrieval
            logger.error(f"Unexpected error in list_tasks: {str(e)}")
            raise RuntimeError(f"Failed to retrieve tasks: {str(e)}")


@mcp_server.call_tool()
async def complete_task_tool(request: CompleteTaskRequest) -> CompleteTaskResponse:
    """
    Mark a task as completed.

    Args:
        request: Contains user_id and task_id

    Returns:
        CompleteTaskResponse with status, task_id, and title
    """
    # Validate inputs
    validate_user_id(request.user_id)
    if request.task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    with get_db_session() as session:
        try:
            task = TaskService.complete_task(
                session=session,
                user_id=request.user_id,
                task_id=request.task_id
            )

            # Add structured logging
            logger.info(f"Task {request.task_id} marked as completed for user {request.user_id}")

            return CompleteTaskResponse(
                status="completed",
                task_id=task.id,
                title=task.title
            )
        except ValueError as e:
            # Propagate ValueError as MCP-friendly error
            logger.error(f"ValueError in complete_task: {str(e)}")
            raise e
        except Exception as e:
            # For other exceptions, wrap in RuntimeError
            logger.error(f"Unexpected error in complete_task: {str(e)}")
            raise RuntimeError(f"Failed to complete task: {str(e)}")


@mcp_server.call_tool()
async def delete_task_tool(request: DeleteTaskRequest) -> DeleteTaskResponse:
    """
    Delete a task.

    Args:
        request: Contains user_id and task_id

    Returns:
        DeleteTaskResponse with status, task_id, and title
    """
    # Validate inputs
    validate_user_id(request.user_id)
    if request.task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    with get_db_session() as session:
        try:
            # First get the task to return its title in the response
            task = TaskService.get_task_by_id(
                session=session,
                user_id=request.user_id,
                task_id=request.task_id
            )

            if not task:
                raise ValueError(f"Task with ID {request.task_id} not found for user {request.user_id}")

            # Delete the task
            TaskService.delete_task(
                session=session,
                user_id=request.user_id,
                task_id=request.task_id
            )

            # Add structured logging
            logger.info(f"Task {request.task_id} deleted for user {request.user_id}")

            return DeleteTaskResponse(
                status="deleted",
                task_id=task.id,
                title=task.title
            )
        except ValueError as e:
            # Propagate ValueError as MCP-friendly error
            logger.error(f"ValueError in delete_task: {str(e)}")
            raise e
        except Exception as e:
            # For other exceptions, wrap in RuntimeError
            logger.error(f"Unexpected error in delete_task: {str(e)}")
            raise RuntimeError(f"Failed to delete task: {str(e)}")


@mcp_server.call_tool()
async def update_task_tool(request: UpdateTaskRequest) -> UpdateTaskResponse:
    """
    Update a task.

    Args:
        request: Contains user_id, task_id, and optional title/description to update

    Returns:
        UpdateTaskResponse with status, task_id, and title
    """
    # Validate inputs
    validate_user_id(request.user_id)
    if request.task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    with get_db_session() as session:
        try:
            # Validate title if provided
            if request.title is not None and request.title.strip() == "":
                raise ValueError("Task title cannot be empty")

            task = TaskService.update_task(
                session=session,
                user_id=request.user_id,
                task_id=request.task_id,
                title=request.title,
                description=request.description
            )

            # Add structured logging
            new_title = request.title if request.title is not None else "unchanged"
            logger.info(f"Task {request.task_id} updated for user {request.user_id} (title: {new_title})")

            return UpdateTaskResponse(
                status="updated",
                task_id=task.id,
                title=task.title
            )
        except ValueError as e:
            # Propagate ValueError as MCP-friendly error
            logger.error(f"ValueError in update_task: {str(e)}")
            raise e
        except Exception as e:
            # For other exceptions, wrap in RuntimeError
            logger.error(f"Unexpected error in update_task: {str(e)}")
            raise RuntimeError(f"Failed to update task: {str(e)}")


def get_mcp_server():
    """Return the MCP server instance"""
    return mcp_server