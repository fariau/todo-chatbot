# Todo AI Chatbot - Google Gemini Integration

## Overview
This project now supports Google Gemini API as the primary LLM provider instead of OpenAI. The integration allows for natural language processing of todo management commands using Google's Gemini 1.5 Flash model.

## Setup Instructions

### 1. Install Dependencies
Make sure you have installed the required dependencies:
```bash
pip install google-generativeai
```

### 2. Configure API Key
1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Update the `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Running the Application
1. Start the backend server:
```bash
cd backend
python main.py
```

2. Start the frontend (in a separate terminal):
```bash
cd frontend
npm run dev
```

## Features

- Natural language processing for todo management
- Support for adding, listing, completing, updating, and deleting tasks
- Conversation history maintained per user
- Error handling for API quota limits
- Responsive UI with chat interface

## Supported Commands

The AI assistant understands various natural language commands:

- **Adding tasks**: "Add a task to buy groceries", "Create a task called 'Finish report'", "Make a new task to call mom"
- **Listing tasks**: "Show my tasks", "List all tasks", "What do I have to do?", "Show pending tasks", "Show completed tasks"
- **Completing tasks**: "Mark task 1 as done", "Complete the shopping task", "Finish the report task"
- **Updating tasks**: "Change task 1 title to 'Updated title'", "Update task 1 description", "Edit the grocery task"
- **Deleting tasks**: "Delete task 1", "Remove the shopping task", "Kill the old task"

## Error Handling

- If the Gemini API quota is exceeded, the system will show a friendly error message
- Network errors and API issues are handled gracefully
- Fallback responses are provided when the API is unavailable

## Architecture

- **Frontend**: Next.js application with Tailwind CSS
- **Backend**: FastAPI server with SQLModel database
- **AI Provider**: Google Gemini 1.5 Flash model
- **Database**: SQLite (can be configured for other databases)

## Environment Variables

Required environment variables in `backend/.env`:
```env
# Database Configuration
DATABASE_URL=sqlite:///./todo_ai_local.db

# Google Gemini Configuration
GEMINI_API_KEY=your_api_key_here

# Application Settings
APP_ENV=development
LOG_LEVEL=info
```

## Troubleshooting

1. **API Key Issues**: Ensure your GEMINI_API_KEY is valid and has sufficient quota
2. **CORS Issues**: The server allows all origins in development mode
3. **Database Issues**: The SQLite database file is created automatically

## Model Configuration

The system uses Gemini 1.5 Flash by default, which provides:
- Fast response times
- Cost-effective usage
- Good understanding of natural language commands
- Reliable function calling for task management