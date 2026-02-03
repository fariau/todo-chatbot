# Task 010: Complete Task MCP Tool

## Task ID: 010
## Title: Complete Task MCP Tool

## Description
Implement the complete_task MCP tool that marks tasks as completed with proper validation and error handling.

## Target Files to Modify/Create
- `backend/src/mcp/tools.py` - Add the complete_task function with proper signature
- Potentially update `backend/src/mcp/server.py` - Register the new tool

## Dependencies
- Task 009 (Previous tool must be implemented)
- Task 005 (Core services must be available)

## Acceptance Criteria
- [ ] complete_task function follows specified signature: complete_task(user_id: str, task_id: int) -> dict
- [ ] Returns proper response format: {"status": "completed", "task_id": int, "title": str}
- [ ] Proper validation for user_id and task_id parameters
- [ ] Error handling for invalid inputs or non-existent tasks
- [ ] Uses todo_service to update task status
- [ ] Tool registers correctly with MCP server
- [ ] Ensures user can only complete their own tasks

## Estimated Complexity
Medium