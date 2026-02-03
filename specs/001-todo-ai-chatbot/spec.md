# Todo AI Chatbot Specification

## Overview
A natural language todo management system that integrates with OpenAI's Agent SDK and MCP protocol to provide conversational task management capabilities. The system follows a completely stateless architecture where all data is persisted in a Neon Serverless PostgreSQL database.

## Data Models

### Task Model
```python
class Task(SQLModel, table=True):
    user_id: str = Field(index=True)                    # Unique identifier for the user (indexed)
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the task
    title: str                                         # Task title (non-null)
    description: Optional[str] = None                  # Optional task description
    completed: bool = Field(default=False)             # Completion status (default: False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of creation
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of last update

    # Constraints: user_id and title must be valid strings, id is auto-generated
```

### Conversation Model
```python
class Conversation(SQLModel, table=True):
    user_id: str = Field(index=True)                   # Unique identifier for the user (indexed)
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the conversation
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of creation
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of last update

    # Constraints: user_id must be valid string, id is auto-generated
```

### Message Model
```python
class Message(SQLModel, table=True):
    user_id: str = Field(index=True)                   # Unique identifier for the user (indexed)
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key for the message
    conversation_id: int = Field(foreign_key="conversation.id", index=True)  # Foreign key to conversation (indexed)
    role: str = Field(regex="^(user|assistant)$")      # Message role (must be "user" or "assistant")
    content: str                                       # Message content (non-null)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of creation

    # Constraints: role must be "user" or "assistant", content must be non-empty
```

## MCP Tools

### add_task
- **Signature**: `add_task(user_id: str, title: str, description: str|None) -> dict`
- **Parameters**:
  - `user_id` (str): Unique identifier for the user
  - `title` (str): Task title (required, non-empty)
  - `description` (str|None): Optional task description
- **Response**: `{"task_id": int, "status": "created", "title": str}`
- **Errors**: Returns error object if user_id is invalid, title is empty, or database error occurs
- **Behavior**: Creates a new task for the specified user with default completed=False status

### list_tasks
- **Signature**: `list_tasks(user_id: str, status: str|None = "all") -> list[dict]`
- **Parameters**:
  - `user_id` (str): Unique identifier for the user
  - `status` (str|None): Filter by status ("all", "completed", "pending") - defaults to "all"
- **Response**: List of task dictionaries with format:
  ```python
  [
    {
      "id": int,
      "user_id": str,
      "title": str,
      "description": str|None,
      "completed": bool,
      "created_at": str (ISO format),
      "updated_at": str (ISO format)
    },
    ...
  ]
  ```
- **Errors**: Returns error object if user_id is invalid or database error occurs
- **Behavior**: Retrieves tasks for the specified user filtered by status

### complete_task
- **Signature**: `complete_task(user_id: str, task_id: int) -> dict`
- **Parameters**:
  - `user_id` (str): Unique identifier for the user
  - `task_id` (int): ID of the task to complete
- **Response**: `{"status": "completed", "task_id": int, "title": str}`
- **Errors**: Returns error object if user_id is invalid, task_id doesn't exist for user, or database error occurs
- **Behavior**: Marks specified task as completed (sets completed=True) and returns confirmation

### delete_task
- **Signature**: `delete_task(user_id: str, task_id: int) -> dict`
- **Parameters**:
  - `user_id` (str): Unique identifier for the user
  - `task_id` (int): ID of the task to delete
- **Response**: `{"status": "deleted", "task_id": int, "title": str}`
- **Errors**: Returns error object if user_id is invalid, task_id doesn't exist for user, or database error occurs
- **Behavior**: Removes specified task and returns confirmation

### update_task
- **Signature**: `update_task(user_id: str, task_id: int, title: str|None, description: str|None) -> dict`
- **Parameters**:
  - `user_id` (str): Unique identifier for the user
  - `task_id` (int): ID of the task to update
  - `title` (str|None): New title (optional, if None keeps current)
  - `description` (str|None): New description (optional, if None keeps current)
- **Response**: `{"status": "updated", "task_id": int, "title": str}`
- **Errors**: Returns error object if user_id is invalid, task_id doesn't exist for user, title is empty, or database error occurs
- **Behavior**: Updates specified task fields and returns confirmation

## API Endpoints

### POST /api/{user_id}/chat
- **Path Parameter**: `user_id` (str): Unique identifier for the user
- **Request Body**:
  ```json
  {
    "conversation_id": int|None,
    "message": str
  }
  ```
  - `conversation_id`: Existing conversation ID or null to start new conversation
  - `message`: User's message content (required, non-empty)
- **Response**:
  ```json
  {
    "conversation_id": int,
    "response": str,
    "tool_calls": [
      {
        "name": str,
        "arguments": dict,
        "result": dict
      }
    ]
  }
  ```
  - `conversation_id`: ID of the conversation (newly created or existing)
  - `response`: AI-generated response to the user
  - `tool_calls`: Array of MCP tools called during processing (empty if none)
- **Logic Steps**:
  1. Validate user_id format and authenticate user
  2. Fetch existing conversation by ID or create new conversation if ID is null
  3. Save user message to conversation history
  4. Retrieve full conversation history for context
  5. Run AI agent with conversation history and registered MCP tools
  6. Capture any tool calls executed by the agent
  7. Save AI assistant response to conversation history
  8. Return response and tool call information
- **Errors**: Returns appropriate HTTP error codes (400 for bad request, 401 for unauthorized, 500 for server errors)

## Agent Behavior

### Intent Recognition
- Maps natural language to appropriate MCP tools:
  - Add/Create/Making/New: "add task X", "create task X", "make task X", "new task X" → add_task
  - Show/List/View/See: "show my tasks", "list tasks", "view pending tasks", "see completed tasks" → list_tasks
  - Done/Complete/Finish/Accept: "mark task X as done", "complete task X", "finish task X" → complete_task
  - Delete/Remove/Kill: "delete task X", "remove task X", "kill task X" → delete_task
  - Change/Update/Edit/Modify: "change task X title", "update task X", "edit task X description" → update_task

### Response Generation
- Friendly, conversational tone with personalized messages
- Confirmation of actions taken: "I've added task 'Buy groceries' for you", "Task 'Call mom' has been marked as completed"
- Error handling with helpful messages: "I couldn't find a task with ID 5. Please check the task ID and try again."
- Follow-up suggestions when appropriate: "Would you like me to show your remaining tasks?"

### Tool Chaining Examples
- Ambiguous delete: "Which task would you like to delete? Let me list your tasks first." → list_tasks followed by delete_task
- Sequential operations: "I'll update your task and then mark it as completed." → update_task followed by complete_task
- Confirmation flow: "I found 3 pending tasks. Which one would you like to complete?" → list_tasks followed by complete_task

### Natural Language Command Examples
- "Add a task to buy milk" → add_task(user_id, "buy milk", None)
- "Show me all my tasks" → list_tasks(user_id, "all")
- "Mark task 5 as completed" → complete_task(user_id, 5)
- "Delete task 3" → delete_task(user_id, 3)
- "Update task 2 to 'Buy groceries and cook dinner'" → update_task(user_id, 2, "Buy groceries and cook dinner", None)

## System Architecture

```
┌─────────────────┐    HTTP Requests     ┌─────────────────┐
│   Frontend      │ ────────────────►   │   Backend       │
│ (ChatKit UI)    │                     │  (FastAPI)      │
└─────────────────┘                     └─────────────────┘
                                               │
                                     API Calls │
                                               ▼
                                    ┌─────────────────┐
                                    │   OpenAI Agent  │
                                    │   (Intent Rec.) │
                                    └─────────────────┘
                                               │
                                      MCP Tool │ Calls
                                               ▼
                                    ┌─────────────────┐
                                    │  MCP Tool Layer │
                                    │  (Stateless)    │
                                    └─────────────────┘
                                               │
                                   SQLModel     │ Sessions
                                               ▼
                                    ┌─────────────────┐
                                    │  PostgreSQL DB  │
                                    │ (Neon Serverless│
                                    │   - Tasks       │
                                    │   - Conversations│
                                    │   - Messages)   │
                                    └─────────────────┘
```

## Frontend Integration

### Chat Interface
- OpenAI ChatKit UI for natural conversation flow
- Real-time messaging capabilities with proper loading states
- Conversation persistence with ability to continue previous conversations
- Responsive design supporting mobile and desktop
- Error handling with user-friendly messages

### Authentication
- Better Auth integration for secure user authentication
- User isolation for data security (users only see their own data)
- Seamless login/logout experience with proper session management
- Automatic user_id passing to backend API calls

## Non-Functional Requirements

### Performance
- API response time < 2 seconds for typical requests
- Database query optimization with proper indexing on user_id fields
- Efficient AI token usage through optimized prompt engineering
- Connection pooling for database connections

### Reliability
- 99.9% uptime target through stateless architecture
- Graceful error handling with fallback responses
- Database transaction safety for all operations
- Proper retry mechanisms for external API calls

### Security
- User data isolation with user_id validation on all requests
- Input sanitization at all API boundaries
- Secure API endpoints with proper authentication
- Encrypted database connections with SSL
- Protection against SQL injection through ORM usage

### Scalability
- Horizontal scaling capability through stateless design
- Database connection pooling for efficient resource usage
- Stateless server architecture allowing multiple instances
- Neon Serverless PostgreSQL for automatic scaling