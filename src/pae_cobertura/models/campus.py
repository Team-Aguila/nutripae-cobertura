from datetime import datetime
from typing import List, Optional
from sqlalchemy import Float
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .institution import Institution
    from .coveragePerMonth import CoveragePerMonth

class Campus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), unique=True, index=True)
    dane_code: str = Field(sa_type=String(13), unique=True, index=True)
    address: str = Field(sa_type=String(255))
    latitude: float = Field(sa_type=Float)
    longitude: float = Field(sa_type=Float)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    institution_id: int = Field(foreign_key="institution.id")
    institution: "Institution" = Relationship(back_populates="campuses")

    coverage_per_month: List["CoveragePerMonth"] = Relationship(back_populates="campus")
