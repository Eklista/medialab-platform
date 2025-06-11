# backend/app/modules/auth/models/invitation.py
"""
Invitation model - System for inviting new users
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class Invitation(BaseModelWithID):
    """
    Invitation model for user registration system
    """
    
    __tablename__ = "invitations"
    
    # Invitation details
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    invited_by_user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Admin who sent invitation
    invited_by_user_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Token and security
    token: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # Hashed invitation token
    
    # Invitation configuration
    target_user_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'internal_user' or 'institutional_user'
    max_uses: Mapped[int] = mapped_column(nullable=False, default=1)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Role assignments (optional pre-configuration)
    suggested_roles: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array of role IDs
    suggested_areas: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array of area IDs (internal users)
    suggested_academic_units: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array of unit IDs (institutional users)
    
    # Status tracking
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    uses_count: Mapped[int] = mapped_column(nullable=False, default=0)
    
    # Usage tracking
    first_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Registration tracking
    registered_user_id: Mapped[int] = mapped_column(Integer, nullable=True)  # User who registered with this invitation
    registered_user_type: Mapped[str] = mapped_column(String(50), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Message and context
    message: Mapped[str] = mapped_column(Text, nullable=True)  # Optional message to invitee
    context: Mapped[str] = mapped_column(String(100), nullable=True)  # onboarding, project_assignment, etc.
    
    # Revocation info
    revoked_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    revoked_by_user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    revocation_reason: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Critical indexes
    __table_args__ = (
        Index("idx_invitation_email", "email"),
        Index("idx_invitation_token", "token"),
        Index("idx_invitation_invited_by", "invited_by_user_id", "invited_by_user_type"),
        Index("idx_invitation_active", "is_active"),
        Index("idx_invitation_expires", "expires_at"),
        Index("idx_invitation_target_type", "target_user_type"),
        Index("idx_invitation_registered", "registered_user_id", "registered_user_type"),
        Index("idx_invitation_email_active", "email", "is_active"),
        Index("idx_invitation_revoked", "revoked_at"),
        Index("idx_invitation_context", "context"),
    )
    
    def __repr__(self) -> str:
        return f"<Invitation(email={self.email}, target_type={self.target_user_type}, active={self.is_active})>"
    
    def is_expired(self) -> bool:
        """Check if invitation is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_exhausted(self) -> bool:
        """Check if invitation has reached max uses"""
        return self.uses_count >= self.max_uses
    
    def can_be_used(self) -> bool:
        """Check if invitation can still be used"""
        return (
            self.is_active and 
            not self.is_expired() and 
            not self.is_exhausted() and 
            self.revoked_at is None
        )
    
    def mark_used(self, user_id: int, user_type: str) -> None:
        """Mark invitation as used"""
        self.uses_count += 1
        self.last_used_at = datetime.utcnow()
        
        if self.uses_count == 1:
            self.first_used_at = self.last_used_at
        
        # If this is a registration (not just viewing)
        if user_id and user_type:
            self.registered_user_id = user_id
            self.registered_user_type = user_type
            self.registered_at = datetime.utcnow()
            
            # Auto-deactivate single-use invitations
            if self.max_uses == 1:
                self.is_active = False
    
    def revoke(self, revoked_by_user_id: int, reason: str = None) -> None:
        """Revoke the invitation"""
        self.is_active = False
        self.revoked_at = datetime.utcnow()
        self.revoked_by_user_id = revoked_by_user_id
        self.revocation_reason = reason