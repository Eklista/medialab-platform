"""
Area model
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class Area(BaseModelWithID):
    """
    Area model for MediaLab internal organization
    """
    
    __tablename__ = "areas"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Classification
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="production")
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Visual identity
    color: Mapped[str] = mapped_column(String(20), nullable=True)
    icon: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Status and configuration
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    
    # Capabilities
    can_lead_projects: Mapped[bool] = mapped_column(nullable=False, default=True)
    requires_collaboration: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Capacity management
    max_concurrent_projects: Mapped[int] = mapped_column(Integer, nullable=True)
    estimated_capacity_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Statistics (updated by services)
    total_members: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active_projects: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_projects: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Contact information
    contact_email: Mapped[str] = mapped_column(String(150), nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Relationships
    user_areas = relationship(
        "UserArea",
        back_populates="area",
        cascade="all, delete-orphan"
    )
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_area_name", "name"),
        Index("idx_area_active", "is_active"),
        Index("idx_area_category", "category"),
        Index("idx_area_can_lead", "can_lead_projects"),
    )
    
    def __repr__(self) -> str:
        return f"<Area(name={self.name})>"