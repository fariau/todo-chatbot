---
id: 25
title: "set-up-llm-config"
stage: "tasks"
date: "2026-01-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-ai-chatbot"
branch: "main"
user: "windows 10"
command: "manual"
labels: ["llm", "configuration", "openai", "agent"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/src/core/llm_config.py"
tests: []
---

# Set Up LLM Configuration

## Original Prompt
```
Task-013 is complete — the MCP tools now have consistent input validation, structured logging, uniform exception handling, and improved observability without altering core logic. Very well executed.

Please proceed to implement **task-014-llm-config.md**.

Instructions:
- Focus on LLM / OpenAI Agents SDK configuration
- Create necessary files (e.g., backend/src/agent/config.py or llm_config.py)
- Set up:
  - OpenAI client initialization (using OPENAI_API_KEY from env)
  - System prompt definition (based on agent behavior spec: natural language → tool mapping, confirmations, error handling, chaining)
  - Agent configuration (model selection, tools registration via get_mcp_server())
  - Optional: temperature, max_tokens, or other inference parameters
- Do NOT implement the full agent runner or chat endpoint yet — focus only on configuration and prompt
- After setup, show the full content of the main LLM/agent config file(s)
- Then ask: "Shall I proceed to task-015-todo-agent.md?"
```

## Response Summary
Successfully set up LLM configuration with OpenAI client initialization, system prompt for the Todo AI agent, agent configuration parameters, and tool definitions for the five required operations. The configuration includes proper environment variable handling and comprehensive system instructions for natural language processing.

## Outcome and Impact
The LLM configuration is now complete with proper OpenAI client setup, system prompt defining agent behavior, and tool definitions for all required operations. This provides a solid foundation for the agent implementation.

## Files Modified
- `backend/src/core/llm_config.py` - LLM configuration with client, system prompt, and tools

## Tests Summary
None yet - configuration setup only

## Next Prompts
LLM configuration complete. Ready to proceed to task-015-todo-agent.md

## Reflection Note
The system prompt clearly defines the agent's capabilities and behavior patterns, which is essential for proper natural language understanding and tool mapping.

## Failure Modes Observed
None observed - all configuration implemented correctly.

## Next Experiment to Improve Prompt Quality
Consider adding validation to ensure the OpenAI API key is properly configured.