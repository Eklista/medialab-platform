"""
Base models with different ID strategies
"""
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, String, Integer, text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session, Mapped, mapped_column


def generate_uuid() -> str:
    """Generate UUID4 string"""
    return str(uuid.uuid4())


@as_declarative()
class BaseModelWithID:
    """
    Base model class with integer ID for internal use only
    Used for: security, organizations modules
    """
    
    # Add this to allow legacy annotations
    __allow_unmapped__ = True
    
    # Primary key as auto-increment integer
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
        comment="Internal unique identifier"
    )
    
    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="Record last update timestamp"
    )
    
    # Audit fields
    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who created this record"
    )
    
    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who last updated this record"
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update_from_dict(self, data: Dict[str, Any], session: Session, updated_by: int = None) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'created_by']:
                setattr(self, key, value)
        
        if updated_by:
            self.updated_by = updated_by
        
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


@as_declarative()
class BaseModelWithUUID:
    """
    Base model class with UUID for public exposure
    Used for: videos, galleries, projects, cms modules
    """
    
    # Add this to allow legacy annotations
    __allow_unmapped__ = True
    
    # Primary key as UUID
    id: Mapped[str] = mapped_column(
        CHAR(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Public unique identifier"
    )
    
    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="Record last update timestamp"
    )
    
    # Audit fields
    created_by: Mapped[Optional[str]] = mapped_column(
        CHAR(36),
        nullable=True,
        comment="User UUID who created this record"
    )
    
    updated_by: Mapped[Optional[str]] = mapped_column(
        CHAR(36),
        nullable=True,
        comment="User UUID who last updated this record"
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update_from_dict(self, data: Dict[str, Any], session: Session, updated_by: str = None) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'created_by']:
                setattr(self, key, value)
        
        if updated_by:
            self.updated_by = updated_by
        
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


@as_declarative()
class BaseModelHybrid:
    """
    Base model class with both ID and UUID
    Used for: users module (internal ID + public UUID)
    """
    
    # Add this to allow legacy annotations
    __allow_unmapped__ = True
    
    # Internal primary key
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
        comment="Internal unique identifier"
    )
    
    # Public UUID
    uuid: Mapped[str] = mapped_column(
        CHAR(36),
        unique=True,
        nullable=False,
        default=generate_uuid,
        index=True,
        comment="Public unique identifier"
    )
    
    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="Record last update timestamp"
    )
    
    # Audit fields
    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who created this record"
    )
    
    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who last updated this record"
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update_from_dict(self, data: Dict[str, Any], session: Session, updated_by: int = None) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'uuid', 'created_at', 'created_by']:
                setattr(self, key, value)
        
        if updated_by:
            self.updated_by = updated_by
        
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, uuid={self.uuid})>"