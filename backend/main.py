from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.core.database import get_session, engine
from src.core.logging import setup_logging
from sqlmodel import Session
from src.api.router import api_router

# Create lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()  # Set up logging
    yield
    # Shutdown
    engine.dispose()


# Create FastAPI app instance
app = FastAPI(
    title="Todo AI Chatbot API",
    description="Natural language todo management system with AI integration",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy"}


# Exception handlers
@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return {"error": "Internal server error", "status": 500}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)