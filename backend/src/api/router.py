from fastapi import APIRouter
from .routes.health import router as health_router
from .routes.chat import router as chat_router

# Create main API router
api_router = APIRouter()

# Include health check route
api_router.include_router(health_router, tags=["health"])

# Include chat route - the chat router already includes user_id in its path
api_router.include_router(chat_router, tags=["chat"])