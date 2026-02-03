# Project Constitution - Todo AI Chatbot

## Core Principles

### 1. Complete Statelessness
- The application server maintains zero in-memory state
- All data (tasks, conversations, messages) stored exclusively in database
- No session persistence on server-side
- No in-memory caching of any kind
- Neon Serverless PostgreSQL as single source of truth
- Every request uses fresh SQLModel Session that's closed after use

### 2. Natural Language Processing
- AI-powered interpretation of user commands using OpenAI Agents SDK
- Intent recognition maps to specific CRUD operations
- Friendly, conversational responses with confirmation after every action
- Error handling with helpful feedback (especially task not found, invalid input)
- Follow OpenAI Agents SDK best practices for conversational flows

### 3. MCP Integration
- Standardized tool interface using Official MCP SDK
- Five core tools exposed: add_task, list_tasks, complete_task, delete_task, update_task
- Stateless tool execution with fresh SQLModel sessions per call
- Consistent input/output contracts following MCP standards
- Proper error handling within tools (return appropriate error messages)

### 4. Type Safety
- Full type hinting everywhere (Python 3.9+ typing)
- Strict typing in function signatures, class definitions, and variable assignments
- Typed dictionaries for API responses using TypedDict
- MyPy compatibility enforced

### 5. Code Quality
- Black formatting for consistent code style
- Docstrings on every public function, class, and module
- Comprehensive error handling with specific exception types
- Proper logging practices with structured logging
- Unit and integration tests for all components
- Follow PEP 8 standards

### 6. Security
- User isolation via user_id validation in all operations
- Better Auth integration for secure user_id validation
- Input validation and sanitization at all boundaries
- Secure database connections with proper authentication
- Environment-based configuration for secrets
- SQL injection prevention through ORM usage

### 7. Performance
- Efficient database queries with proper indexing
- Minimal API response times through optimized queries
- Connection pooling for database connections
- No unnecessary data loading or processing

### 8. Maintainability
- Clear separation of concerns (models, services, API, tools)
- Modular architecture with single responsibility principle
- Consistent naming conventions throughout codebase
- Documentation for all public interfaces and complex logic
- Follow FastAPI best practices for API design

## Technology Stack

### Backend
- Python 3.9+
- FastAPI for web framework
- SQLModel for ORM (combining SQLAlchemy + Pydantic)
- Neon Serverless PostgreSQL for database
- OpenAI SDK for AI integration
- Official MCP SDK for tool exposure
- Pydantic for data validation

### Frontend
- OpenAI ChatKit UI
- TypeScript for type safety
- React for component architecture
- Next.js for server-side rendering

### Authentication
- Better Auth for user management
- User_id based access control with validation
- Secure session management

## Architectural Constraints

1. **Database-First Design**: All state originates from database
2. **API Contract Consistency**: Fixed input/output schemas with proper validation
3. **Tool Standardization**: MCP tools follow specific signature patterns and error handling
4. **No In-Memory State**: Server maintains no persistent state between requests
5. **Error Transparency**: Clear, specific error messages for debugging
6. **Scalability**: Designed for horizontal scaling with stateless architecture
7. **Observability**: Built-in logging and monitoring capabilities
8. **Security First**: User isolation and input validation at every layer