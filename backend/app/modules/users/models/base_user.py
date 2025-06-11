"""
Base User model with common fields for all user types
"""
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelHybrid


class BaseUser(BaseModelHybrid):
    """
    Abstract base user model with common fields for all user types
    Uses hybrid ID strategy (internal ID + public UUID)
    """
    
    __abstract__ = True
    
    # Authentication fields
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Unique username for login"
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="Email address (also used for login)"
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Hashed password"
    )
    
    # Personal information
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="User's first name"
    )
    
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="User's last name"
    )
    
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Contact phone number"
    )
    
    # Profile information
    profile_photo: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL or path to profile photo"
    )
    
    birthday: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Date of birth"
    )
    
    # Status and tracking
    join_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
        comment="Date when user joined the platform"
    )
    
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="Last login timestamp"
    )
    
    # Account status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether account is active (Y/N)"
    )
    
    is_verified: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether email is verified (Y/N)"
    )
    
    is_locked: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether account is locked (Y/N)"
    )
    
    # Password reset
    reset_token: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Password reset token"
    )
    
    reset_token_expires: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="Password reset token expiration"
    )
    
    # Additional information
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="User biography or description"
    )
    
    timezone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default="America/Guatemala",
        comment="User's timezone"
    )
    
    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="es",
        comment="Preferred language (es, en)"
    )
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_name(self) -> str:
        """Get display name (first name + last name or username if empty)"""
        if self.first_name and self.last_name:
            return self.full_name
        return self.username
    
    @property
    def is_account_active(self) -> bool:
        """Check if account is fully active"""
        return (
            self.is_active == "Y" and 
            self.is_verified == "Y" and 
            self.is_locked == "N"
        )
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(username={self.username}, email={self.email})>"