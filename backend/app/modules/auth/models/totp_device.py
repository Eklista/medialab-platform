# backend/app/modules/auth/models/totp_device.py
"""
TOTP Device model - 2FA TOTP devices for users
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class TotpDevice(BaseModelWithID):
    """
    TOTP Device model for 2FA authentication
    """
    
    __tablename__ = "totp_devices"
    
    # User relationship (polymorphic)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'internal_user' or 'institutional_user'
    
    # Device identification
    device_name: Mapped[str] = mapped_column(String(100), nullable=False)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    
    # TOTP configuration
    secret_key: Mapped[str] = mapped_column(String(32), nullable=False)  # Base32 encoded secret
    algorithm: Mapped[str] = mapped_column(String(10), nullable=False, default="SHA1")
    digits: Mapped[int] = mapped_column(nullable=False, default=6)
    period: Mapped[int] = mapped_column(nullable=False, default=30)  # seconds
    
    # Device status
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Usage tracking
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    use_count: Mapped[int] = mapped_column(nullable=False, default=0)
    
    # Verification process
    verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    setup_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Security
    last_counter: Mapped[int] = mapped_column(nullable=False, default=0)  # Prevent replay attacks
    
    # Critical indexes
    __table_args__ = (
        Index("idx_totp_device_user", "user_id", "user_type"),
        Index("idx_totp_device_active", "is_active"),
        Index("idx_totp_device_verified", "is_verified"),
        Index("idx_totp_device_user_active", "user_id", "user_type", "is_active"),
        Index("idx_totp_device_user_verified", "user_id", "user_type", "is_verified"),
        Index("idx_totp_device_device_id", "device_id"),
        Index("idx_totp_device_primary", "user_id", "user_type", "is_primary"),
    )
    
    def __repr__(self) -> str:
        return f"<TotpDevice(user_id={self.user_id}, name={self.device_name}, verified={self.is_verified})>"
    
    def mark_as_used(self, counter: int) -> None:
        """Mark device as used with counter"""
        self.last_used_at = datetime.utcnow()
        self.use_count += 1
        self.last_counter = counter
    
    def verify_device(self) -> None:
        """Mark device as verified"""
        self.is_verified = True
        self.verified_at = datetime.utcnow()
        self.setup_completed_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the device"""
        self.is_active = False
        self.is_primary = False