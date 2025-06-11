# backend/app/modules/auth/models/oauth_account.py
"""
OAuth Account model - Links OAuth accounts to users
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class OAuthAccount(BaseModelWithID):
    """
    OAuth Account model for linking external OAuth accounts
    """
    
    __tablename__ = "oauth_accounts"
    
    # User relationship (polymorphic)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'internal_user' or 'institutional_user'
    
    # OAuth provider info
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # google, microsoft, etc.
    provider_user_id: Mapped[str] = mapped_column(String(100), nullable=False)  # OAuth provider's user ID
    provider_username: Mapped[str] = mapped_column(String(100), nullable=True)  # OAuth provider's username
    
    # Profile information from OAuth
    provider_email: Mapped[str] = mapped_column(String(150), nullable=True)
    provider_name: Mapped[str] = mapped_column(String(200), nullable=True)
    provider_picture: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # OAuth tokens (encrypted in production)
    access_token: Mapped[str] = mapped_column(Text, nullable=True)  # Encrypted OAuth access token
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)  # Encrypted OAuth refresh token
    token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Account status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)  # Primary OAuth account
    
    # Usage tracking
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    login_count: Mapped[int] = mapped_column(nullable=False, default=0)
    
    # Linking info
    linked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    linked_ip: Mapped[str] = mapped_column(String(45), nullable=True)
    
    # Scope and permissions granted
    granted_scopes: Mapped[str] = mapped_column(String(500), nullable=True)  # Space-separated scopes
    
    # Provider-specific metadata
    provider_metadata: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    
    # Critical indexes
    __table_args__ = (
        Index("idx_oauth_account_user", "user_id", "user_type"),
        Index("idx_oauth_account_provider", "provider"),
        Index("idx_oauth_account_provider_user", "provider", "provider_user_id"),
        Index("idx_oauth_account_active", "is_active"),
        Index("idx_oauth_account_verified", "is_verified"),
        Index("idx_oauth_account_user_active", "user_id", "user_type", "is_active"),
        Index("idx_oauth_account_user_primary", "user_id", "user_type", "is_primary"),
        Index("idx_oauth_account_provider_email", "provider_email"),
        Index("idx_oauth_account_last_login", "last_login_at"),
    )
    
    def __repr__(self) -> str:
        return f"<OAuthAccount(user_id={self.user_id}, provider={self.provider}, active={self.is_active})>"
    
    def mark_login(self) -> None:
        """Mark OAuth account as used for login"""
        self.last_login_at = datetime.utcnow()
        self.login_count += 1
    
    def update_tokens(self, access_token: str, refresh_token: str = None, expires_at: datetime = None) -> None:
        """Update OAuth tokens"""
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        if expires_at:
            self.token_expires_at = expires_at
    
    def is_token_expired(self) -> bool:
        """Check if OAuth token is expired"""
        if self.token_expires_at is None:
            return False
        return datetime.utcnow() > self.token_expires_at
    
    def deactivate(self) -> None:
        """Deactivate OAuth account"""
        self.is_active = False
        self.is_primary = False