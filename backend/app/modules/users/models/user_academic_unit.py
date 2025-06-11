"""
UserAcademicUnit model - Base unificado
"""
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class UserAcademicUnit(BaseModelWithID):
    """
    Many-to-many relationship between institutional users and academic units
    """
    
    __tablename__ = "user_academic_units"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutional_users.id", ondelete="CASCADE"), nullable=False)
    academic_unit_id: Mapped[int] = mapped_column(Integer, ForeignKey("academic_units.id", ondelete="CASCADE"), nullable=False)
    
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False, default="member")
    position_title: Mapped[str] = mapped_column(String(150), nullable=True)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    
    degree_program: Mapped[str] = mapped_column(String(200), nullable=True)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=True)
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    can_represent_unit: Mapped[bool] = mapped_column(nullable=False, default=False)
    has_budget_authority: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    office_number: Mapped[str] = mapped_column(String(50), nullable=True)
    internal_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relationships
    user = relationship("InstitutionalUser", back_populates="user_academic_units")
    academic_unit = relationship("AcademicUnit", back_populates="user_academic_units")
    
    __table_args__ = (
        UniqueConstraint("user_id", "academic_unit_id", name="uq_user_academic_unit"),
        Index("idx_user_academic_unit_user", "user_id"),
        Index("idx_user_academic_unit_unit", "academic_unit_id"),
        Index("idx_user_academic_unit_active", "is_active"),
        Index("idx_user_academic_unit_user_active", "user_id", "is_active"),
        Index("idx_user_academic_unit_unit_active", "academic_unit_id", "is_active"),
        Index("idx_user_academic_unit_primary", "user_id", "is_primary"),
        Index("idx_user_academic_unit_represent", "user_id", "can_represent_unit"),
        Index("idx_user_academic_unit_budget", "user_id", "has_budget_authority"),
        Index("idx_user_academic_unit_relationship", "relationship_type"),
    )
    
    def __repr__(self) -> str:
        return f"<UserAcademicUnit(user_id={self.user_id}, unit_id={self.academic_unit_id})>"