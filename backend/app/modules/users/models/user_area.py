"""
UserArea model
"""
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.shared.base.base_model import BaseModelWithID

if TYPE_CHECKING:
    from .internal_user import InternalUser
    from app.modules.organizations.models import Area


class UserArea(BaseModelWithID):
    """
    Many-to-many relationship between internal users and areas
    """
    
    __tablename__ = "user_areas"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("internal_users.id", ondelete="CASCADE"), nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey("areas.id", ondelete="CASCADE"), nullable=False)
    
    role_in_area: Mapped[str] = mapped_column(String(100), nullable=True)
    specialization: Mapped[str] = mapped_column(String(150), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    can_lead_projects: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    time_allocation_percentage: Mapped[int] = mapped_column(nullable=True)
    
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    assignment_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user = relationship("InternalUser", back_populates="user_areas")
    area = relationship("Area", back_populates="user_areas")
    
    __table_args__ = (
        UniqueConstraint("user_id", "area_id", name="uq_user_area"),
        Index("idx_user_area_user", "user_id"),
        Index("idx_user_area_area", "area_id"),
        Index("idx_user_area_active", "is_active"),
        Index("idx_user_area_user_active", "user_id", "is_active"),
        Index("idx_user_area_area_active", "area_id", "is_active"),
        Index("idx_user_area_primary", "user_id", "is_primary"),
        Index("idx_user_area_can_lead", "user_id", "can_lead_projects"),
    )
    
    def __repr__(self) -> str:
        return f"<UserArea(user_id={self.user_id}, area_id={self.area_id})>"