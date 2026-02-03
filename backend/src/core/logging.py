import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Set up logging configuration
def setup_logging(level: str = "INFO"):
    """
    Set up centralized logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Add handler if not already added
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    # Set specific loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger

    Returns:
        Configured Logger instance
    """
    return logging.getLogger(name)


def log_error(error: Exception, context: str = "", extra_data: Dict[str, Any] = None):
    """
    Log an error with context and additional data.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        extra_data: Additional data to include in the log
    """
    logger = get_logger(__name__)

    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if extra_data:
        error_info.update(extra_data)

    logger.error(f"Error occurred: {error_info}")


def log_api_call(endpoint: str, user_id: str, status_code: int, duration_ms: float):
    """
    Log API call information.

    Args:
        endpoint: The API endpoint that was called
        user_id: The user ID making the request
        status_code: The HTTP status code returned
        duration_ms: The duration of the request in milliseconds
    """
    logger = get_logger(__name__)

    log_data = {
        "endpoint": endpoint,
        "user_id": user_id,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "timestamp": datetime.utcnow().isoformat(),
    }

    logger.info(f"API call: {log_data}")


def log_tool_execution(tool_name: str, user_id: str, success: bool, duration_ms: float, error_msg: str = None):
    """
    Log MCP tool execution.

    Args:
        tool_name: Name of the tool that was executed
        user_id: The user ID associated with the tool call
        success: Whether the tool execution was successful
        duration_ms: The duration of the tool execution in milliseconds
        error_msg: Error message if the execution failed
    """
    logger = get_logger(__name__)

    log_data = {
        "tool_name": tool_name,
        "user_id": user_id,
        "success": success,
        "duration_ms": duration_ms,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if error_msg:
        log_data["error"] = error_msg

    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Tool execution {status}: {log_data}")