---
id: 9
title: "initial-project-setup"
stage: "spec"
date: "2026-01-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-ai-chatbot"
branch: "main"
user: "windows 10"
command: "sp.phr"
labels: ["initialization", "project", "setup", "specification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "CLAUDE.md"
  - "specs/001-todo-ai-chatbot/constitution.md"
  - "specs/001-todo-ai-chatbot/spec.md"
tests: []
---

# Initial Project Setup

## Original Prompt
```
You are an expert AI coding assistant following strict Spec-Driven Development (SDD) principles using Spec-Kit Plus methodology.

Project: Todo AI Chatbot (Phase III)
Goal: Build a stateless, natural language todo manager using:
- Backend: Python FastAPI
- AI: OpenAI Agents SDK (agent + runner)
- MCP: Official MCP SDK (expose CRUD tools: add_task, list_tasks, complete_task, delete_task, update_task)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL (stateless sessions only)
- Frontend: OpenAI ChatKit UI
- Auth: Better Auth (user_id based)
- All state persisted in DB (tasks, conversations, messages) — server is fully stateless

Key requirements (follow exactly):
1. Database models:
   - Task: user_id (str), id (PK), title (str), description (str|None), completed (bool default False), created_at, updated_at
   - Conversation: user_id (str), id (PK), created_at, updated_at
   - Message: user_id (str), id (PK), conversation_id (FK), role ("user"|"assistant"), content (str), created_at

2. MCP Tools (stateless, use SQLModel Session each call):
   - add_task(user_id: str, title: str, description: str|None) → {"task_id": int, "status": "created", "title": str}
   - list_tasks(user_id: str, status: str|None = "all") → list of task dicts
   - complete_task(user_id: str, task_id: int) → update completed=True
   - delete_task(user_id: str, task_id: int)
   - update_task(user_id: str, task_id: int, title: str|None, description: str|None)

3. Chat endpoint: POST /api/{user_id}/chat
   - Body: {"conversation_id": int|None, "message": str}
   - Fetch/create conversation, save user message, run agent with history + new message + MCP tools, save assistant response, return {"conversation_id", "response", "tool_calls"}

4. Agent behavior:
   - Map natural language to tools (add/create → add_task, show/list → list_tasks, done/complete → complete_task, delete/remove → delete_task, change/update → update_task)
   - Always confirm actions friendly
   - Handle errors (task not found, etc.)
   - Chain tools if needed (e.g., list before ambiguous delete)

5. Architecture: Stateless FastAPI server, DB persistence for conversations & tasks, ChatKit frontend with domain key.

First actions:
1. Create folder structure in current directory:
   - backend/ (main.py, routers/, models.py, mcp/, database.py)
   - frontend/ (for ChatKit config)
   - specs/ (constitution.md, spec.md, plan.md, tasks/)
   - .env.example, README.md

2. Write CLAUDE.md in root with project overview, rules (stateless only, type hints, black format, docstrings, error handling, no manual state)

3. Write initial constitution.md in specs/ with core principles from above

4. Write high-level spec.md summarizing models, endpoints, tools, behaviors

5. Suggest next step: generate detailed plan.md

Output step-by-step:
- Show folder structure you will create
- Full content for CLAUDE.md
- Full content for specs/constitution.md
- Full content for specs/spec.md
- Then ask: "Shall I proceed to create plan.md?"

Do NOT write any Python code yet — focus on documentation and planning first.
```

## Response Summary
Successfully initiated the Todo AI Chatbot project following SDD principles. Created the required folder structure and documentation files (CLAUDE.md, constitution.md, spec.md) establishing the foundation for the stateless, natural language todo manager with MCP integration.

## Outcome and Impact
The Todo AI Chatbot Phase III project has been properly initiated with comprehensive specifications and documentation. The stateless architecture with natural language processing using OpenAI Agents and MCP tools has been clearly defined, providing a solid foundation for implementation.

## Files Modified
- `CLAUDE.md` - Project overview and rules
- `specs/001-todo-ai-chatbot/constitution.md` - Core principles
- `specs/001-todo-ai-chatbot/spec.md` - High-level specifications

## Tests Summary
None yet - specification and planning only

## Next Prompts
Ready to proceed with creating plan.md for detailed implementation roadmap.

## Reflection Note
Following SDD methodology from the beginning ensures clear requirements and architecture before implementation begins. This prevents scope creep and ensures all stakeholders have aligned expectations.

## Failure Modes Observed
None observed - all specifications were captured accurately in the documentation.

## Next Experiment to Improve Prompt Quality
Consider adding validation steps to ensure all architectural constraints are explicitly addressed in the specification.