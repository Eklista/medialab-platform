"""
UserArea model for assigning internal users to MediaLab areas
"""
from sqlalchemy import Integer, String, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date

from app.shared.base.base_model import BaseModelWithID


class UserArea(BaseModelWithID):
    """
    Many-to-many relationship table between internal users and areas
    Only applies to InternalUser (MediaLab staff)
    """
    
    __tablename__ = "user_areas"
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("internal_users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to internal users table"
    )
    
    area_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("areas.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to areas table"
    )
    
    # Assignment details
    role_in_area: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Specific role within this area (Lead, Specialist, Assistant, etc.)"
    )
    
    specialization: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        comment="Specific specialization within the area"
    )
    
    # Status and priority
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether area assignment is active (Y/N)"
    )
    
    is_primary: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether this is the user's primary area (Y/N)"
    )
    
    can_lead_projects: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether user can lead projects in this area (Y/N)"
    )
    
    # Time allocation
    time_allocation_percentage: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Percentage of time allocated to this area (0-100)"
    )
    
    # Assignment metadata
    assignment_reason: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Reason for area assignment"
    )
    
    start_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Start date of assignment"
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="End date of assignment (if temporary)"
    )
    
    # Relationships
    user = relationship(
        "InternalUser",
        back_populates="user_areas"
    )
    
    area = relationship(
        "Area",
        back_populates="user_areas"
    )
    
    # Constraints and indexes
    __table_args__ = (
        # Unique constraint to prevent duplicate user-area pairs
        UniqueConstraint(
            "user_id", 
            "area_id", 
            name="uq_user_area"
        ),
        
        # Indexes for performance
        Index("idx_user_area_user", "user_id"),
        Index("idx_user_area_area", "area_id"),
        Index("idx_user_area_active", "is_active"),
        Index("idx_user_area_primary", "is_primary"),
        Index("idx_user_area_can_lead", "can_lead_projects"),
        Index("idx_user_area_user_active", "user_id", "is_active"),
        Index("idx_user_area_area_active", "area_id", "is_active"),
        Index("idx_user_area_user_primary", "user_id", "is_primary"),
        Index("idx_user_area_active_can_lead", "is_active", "can_lead_projects"),
        Index("idx_user_area_start_date", "start_date"),
        Index("idx_user_area_end_date", "end_date"),
    )
    
    def __repr__(self) -> str:
        return f"<UserArea(user_id={self.user_id}, area_id={self.area_id}, role={self.role_in_area})>"