"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import get_settings

# Get database settings
settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database.URL,
    echo=settings.database.ECHO,
    pool_size=settings.database.POOL_SIZE,
    max_overflow=settings.database.MAX_OVERFLOW,
    pool_timeout=settings.database.POOL_TIMEOUT,
    pool_recycle=settings.database.POOL_RECYCLE,
    pool_pre_ping=True,  # Validate connections before use
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI
    Creates a new database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all tables (for development/testing)
    In production, use Alembic migrations
    """
    # Import models to register them with SQLAlchemy
    import app.modules.users.models
    import app.modules.organizations.models
    import app.modules.security.models
    import app.modules.cms.models
    
    from app.shared.base.base_model import BaseModelWithID, BaseModelWithUUID, BaseModelHybrid
    
    # Create tables for all base models
    BaseModelWithID.metadata.create_all(bind=engine)
    BaseModelWithUUID.metadata.create_all(bind=engine)
    BaseModelHybrid.metadata.create_all(bind=engine)


def check_database_connection() -> bool:
    """
    Check if database connection is working
    """
    try:
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False