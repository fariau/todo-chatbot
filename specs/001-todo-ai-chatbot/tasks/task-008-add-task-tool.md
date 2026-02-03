# Task 008: Add Task MCP Tool

## Task ID: 008
## Title: Add Task MCP Tool

## Description
Implement the add_task MCP tool that creates new tasks for users with proper validation and error handling.

## Target Files to Modify/Create
- `backend/src/mcp/tools.py` - Add the add_task function with proper signature
- Potentially update `backend/src/mcp/server.py` - Register the new tool

## Dependencies
- Task 007 (MCP framework must be set up)
- Task 005 (Core services must be available)

## Acceptance Criteria
- [ ] add_task function follows specified signature: add_task(user_id: str, title: str, description: str|None) -> dict
- [ ] Returns proper response format: {"task_id": int, "status": "created", "title": str}
- [ ] Proper validation for user_id and title parameters
- [ ] Error handling for invalid inputs
- [ ] Uses todo_service to create tasks
- [ ] Tool registers correctly with MCP server
- [ ] Tool handles database errors appropriately

## Estimated Complexity
Medium