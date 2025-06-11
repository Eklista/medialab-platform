# backend/app/modules/auth/models/backup_code.py
"""
Backup Code model - 2FA backup codes for users
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class BackupCode(BaseModelWithID):
    """
    Backup Code model for 2FA recovery
    """
    
    __tablename__ = "backup_codes"
    
    # User relationship (polymorphic)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'internal_user' or 'institutional_user'
    
    # Code details
    code: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)  # Hashed backup code
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # Bcrypt hash of the code
    
    # Status
    is_used: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Usage tracking
    used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    used_ip: Mapped[str] = mapped_column(String(45), nullable=True)
    used_user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Generation info
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Optional expiration
    
    # Batch tracking (codes are generated in batches)
    batch_id: Mapped[str] = mapped_column(String(64), nullable=False)
    sequence_number: Mapped[int] = mapped_column(nullable=False)  # Position in batch (1-10)
    
    # Critical indexes
    __table_args__ = (
        Index("idx_backup_code_user", "user_id", "user_type"),
        Index("idx_backup_code_code", "code"),
        Index("idx_backup_code_used", "is_used"),
        Index("idx_backup_code_active", "is_active"),
        Index("idx_backup_code_user_active", "user_id", "user_type", "is_active"),
        Index("idx_backup_code_user_unused", "user_id", "user_type", "is_used"),
        Index("idx_backup_code_batch", "batch_id"),
        Index("idx_backup_code_expires", "expires_at"),
    )
    
    def __repr__(self) -> str:
        return f"<BackupCode(user_id={self.user_id}, used={self.is_used}, batch={self.batch_id})>"
    
    def mark_as_used(self, ip_address: str, user_agent: str) -> None:
        """Mark backup code as used"""
        self.is_used = True
        self.used_at = datetime.utcnow()
        self.used_ip = ip_address
        self.used_user_agent = user_agent
    
    def is_expired(self) -> bool:
        """Check if backup code is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def deactivate(self) -> None:
        """Deactivate the backup code"""
        self.is_active = False