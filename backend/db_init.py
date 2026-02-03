from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
import os
from src.models import task, conversation, message
from src.core.database import engine

def init_db():
    """Initialize the database by creating all tables."""
    try:
        print("Creating database tables...")
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except SQLAlchemyError as e:
        print(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()