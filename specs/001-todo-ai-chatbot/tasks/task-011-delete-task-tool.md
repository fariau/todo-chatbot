# Task 011: Delete Task MCP Tool

## Task ID: 011
## Title: Delete Task MCP Tool

## Description
Implement the delete_task MCP tool that removes tasks with proper validation and error handling.

## Target Files to Modify/Create
- `backend/src/mcp/tools.py` - Add the delete_task function with proper signature
- Potentially update `backend/src/mcp/server.py` - Register the new tool

## Dependencies
- Task 010 (Previous tool must be implemented)
- Task 005 (Core services must be available)

## Acceptance Criteria
- [ ] delete_task function follows specified signature: delete_task(user_id: str, task_id: int) -> dict
- [ ] Returns proper response format: {"status": "deleted", "task_id": int, "title": str}
- [ ] Proper validation for user_id and task_id parameters
- [ ] Error handling for invalid inputs or non-existent tasks
- [ ] Uses todo_service to delete tasks
- [ ] Tool registers correctly with MCP server
- [ ] Ensures user can only delete their own tasks

## Estimated Complexity
Medium