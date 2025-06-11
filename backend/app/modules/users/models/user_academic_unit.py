"""
UserAcademicUnit model for assigning institutional users to academic units
"""
from sqlalchemy import Integer, String, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date

from app.shared.base.base_model import BaseModelWithID


class UserAcademicUnit(BaseModelWithID):
    """
    Many-to-many relationship table between institutional users and academic units
    Only applies to InstitutionalUser (faculty, students, external clients)
    """
    
    __tablename__ = "user_academic_units"
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("institutional_users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to institutional users table"
    )
    
    academic_unit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("academic_units.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to academic units table"
    )
    
    # Relationship details
    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="member",
        comment="Type of relationship (faculty, student, staff, collaborator, external)"
    )
    
    position_title: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        comment="Specific position or title within the academic unit"
    )
    
    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Specific department within the academic unit"
    )
    
    # Academic information
    degree_program: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Degree program (for students)"
    )
    
    academic_year: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Academic year or level"
    )
    
    graduation_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Expected or actual graduation date"
    )
    
    # Status and permissions
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether assignment is active (Y/N)"
    )
    
    is_primary: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether this is the user's primary academic unit (Y/N)"
    )
    
    can_represent_unit: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether user can represent the academic unit (Y/N)"
    )
    
    has_budget_authority: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether user has budget authority for projects (Y/N)"
    )
    
    # Time periods
    start_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Start date of association"
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="End date of association (if applicable)"
    )
    
    # Contact within unit
    office_number: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Office number within the academic unit"
    )
    
    internal_phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Internal phone extension"
    )
    
    # Relationships
    user = relationship(
        "InstitutionalUser",
        back_populates="user_academic_units"
    )
    
    academic_unit = relationship(
        "AcademicUnit",
        back_populates="user_academic_units"
    )
    
    # Constraints and indexes
    __table_args__ = (
        # Unique constraint to prevent duplicate user-academic unit pairs
        UniqueConstraint(
            "user_id", 
            "academic_unit_id", 
            name="uq_user_academic_unit"
        ),
        
        # Indexes for performance
        Index("idx_user_academic_unit_user", "user_id"),
        Index("idx_user_academic_unit_academic_unit", "academic_unit_id"),
        Index("idx_user_academic_unit_relationship_type", "relationship_type"),
        Index("idx_user_academic_unit_active", "is_active"),
        Index("idx_user_academic_unit_primary", "is_primary"),
        Index("idx_user_academic_unit_can_represent", "can_represent_unit"),
        Index("idx_user_academic_unit_budget_authority", "has_budget_authority"),
        Index("idx_user_academic_unit_user_active", "user_id", "is_active"),
        Index("idx_user_academic_unit_unit_active", "academic_unit_id", "is_active"),
        Index("idx_user_academic_unit_user_primary", "user_id", "is_primary"),
        Index("idx_user_academic_unit_type_active", "relationship_type", "is_active"),
        Index("idx_user_academic_unit_start_date", "start_date"),
        Index("idx_user_academic_unit_end_date", "end_date"),
        Index("idx_user_academic_unit_graduation", "graduation_date"),
    )
    
    def __repr__(self) -> str:
        return f"<UserAcademicUnit(user_id={self.user_id}, unit_id={self.academic_unit_id}, type={self.relationship_type})>"