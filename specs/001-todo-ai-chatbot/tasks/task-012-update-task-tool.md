# Task 012: Update Task MCP Tool

## Task ID: 012
## Title: Update Task MCP Tool

## Description
Implement the update_task MCP tool that modifies task properties with proper validation and error handling.

## Target Files to Modify/Create
- `backend/src/mcp/tools.py` - Add the update_task function with proper signature
- Potentially update `backend/src/mcp/server.py` - Register the new tool

## Dependencies
- Task 011 (Previous tool must be implemented)
- Task 005 (Core services must be available)

## Acceptance Criteria
- [ ] update_task function follows specified signature: update_task(user_id: str, task_id: int, title: str|None, description: str|None) -> dict
- [ ] Returns proper response format: {"status": "updated", "task_id": int, "title": str}
- [ ] Proper validation for user_id and task_id parameters
- [ ] Partial updates work correctly (only update provided fields)
- [ ] Error handling for invalid inputs or non-existent tasks
- [ ] Uses todo_service to update tasks
- [ ] Tool registers correctly with MCP server
- [ ] Ensures user can only update their own tasks

## Estimated Complexity
Medium