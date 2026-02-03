from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure SSL is enabled for Neon PostgreSQL
if DATABASE_URL and "neon.tech" in DATABASE_URL and "sslmode=require" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# For SQLite, we need to use StaticPool instead of QueuePool
if DATABASE_URL.startswith("sqlite"):
    # Use StaticPool for SQLite (better for file-based databases)
    engine: Engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
    )
else:
    # Create engine with connection pooling for performance (for PostgreSQL)
    engine: Engine = create_engine(
        DATABASE_URL,
        echo=False,
        poolclass=QueuePool,
        pool_size=10,           # Number of connections to maintain
        max_overflow=20,        # Additional connections beyond pool_size
        pool_pre_ping=True,     # Verify connections before use
        pool_recycle=300        # Recycle connections after 5 minutes
    )


def get_session():
    with Session(engine) as session:
        yield session