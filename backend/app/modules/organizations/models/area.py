"""
Area model - Simple version for MediaLab internal organization
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class Area(BaseModelWithID):
    """
    Simple Area model for MediaLab internal staff organization
    Used for dashboard display: "Pablo Lacan - Transmisión"
    
    Examples:
    - Transmisión
    - Producción Audiovisual  
    - Diseño Gráfico
    - Motion Graphics
    """
    
    __tablename__ = "areas"
    
    # Core fields only
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        comment="Area name"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Area description"
    )
    
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Active status"
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        comment="Display order"
    )
    
    # relationship with internal users
    user_areas = relationship(
        "UserArea",
        back_populates="area",
        cascade="all, delete-orphan"
    )
    
    # Simple indexes
    __table_args__ = (
        Index("idx_area_name", "name"),
        Index("idx_area_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<Area(name={self.name})>"