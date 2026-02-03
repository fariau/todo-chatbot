# Todo AI Chatbot

A full-stack application combining a FastAPI backend with a Next.js frontend to create an intelligent todo management system with AI capabilities.

## Project Structure

```
todo-ai-chatbot/
├── backend/           # FastAPI backend with AI integration
├── frontend/          # Next.js frontend with Tailwind CSS
└── README.md
```

## Features

- AI-powered todo management
- Full-stack application with modern technologies
- Responsive UI with Tailwind CSS
- FastAPI backend with asynchronous capabilities
- Natural language task management
- MCP-integrated tools (add, list, complete, delete, update tasks)
- Conversation persistence
- User isolation
- State-of-the-art AI intent recognition

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the backend directory with the required configuration.

6. Initialize the database:
   ```bash
   python db_init.py
   ```

7. Run the backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Frontend Setup (Next.js)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables:
   Create a `.env.local` file in the frontend directory with the required configuration.

4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Architecture

- **Backend**: Python FastAPI server
- **AI**: OpenAI Agents SDK with MCP tools
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Frontend**: OpenAI ChatKit UI
- **Authentication**: Better Auth

## MCP Tools

The system exposes 5 core tools via MCP protocol:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve tasks
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks
- `update_task`: Modify existing tasks

## Environment Variables

See `.env.example` for required environment variables.

## Development

This project follows Spec-Driven Development (SDD) methodology with comprehensive documentation in the `specs/` directory.

## Deployment

### GitHub Pages

The frontend is automatically deployed to GitHub Pages using GitHub Actions. When changes are pushed to the main branch, the workflow will:

1. Build the Next.js application for static export
2. Deploy the static files to the `gh-pages` branch
3. Host the site at `https://fariau.github.io/todo-chatbot/`

To manually trigger deployment, you can run:
```bash
cd frontend
npm run build-gh-pages
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.