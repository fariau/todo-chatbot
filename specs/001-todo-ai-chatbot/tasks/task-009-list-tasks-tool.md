# Task 009: List Tasks MCP Tool

## Task ID: 009
## Title: List Tasks MCP Tool

## Description
Implement the list_tasks MCP tool that retrieves tasks for users with status filtering and proper error handling.

## Target Files to Modify/Create
- `backend/src/mcp/tools.py` - Add the list_tasks function with proper signature
- Potentially update `backend/src/mcp/server.py` - Register the new tool

## Dependencies
- Task 008 (Previous tool must be implemented)
- Task 005 (Core services must be available)

## Acceptance Criteria
- [ ] list_tasks function follows specified signature: list_tasks(user_id: str, status: str|None = "all") -> list[dict]
- [ ] Returns proper response format with complete task objects
- [ ] Proper status filtering ("all", "completed", "pending")
- [ ] Proper validation for user_id parameter
- [ ] Error handling for invalid inputs
- [ ] Uses todo_service to retrieve tasks
- [ ] Tool registers correctly with MCP server

## Estimated Complexity
Medium