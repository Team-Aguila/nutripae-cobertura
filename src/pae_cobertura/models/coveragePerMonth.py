from datetime import datetime, date
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel, Date
import uuid
from uuid import UUID

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .campus import Campus
    from .coverage import Coverage

class CoveragePerMonth(SQLModel, table=True):
    __tablename__ = "coveragePerMonth"

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_start: date = Field(sa_type=Date(), index=True)
    date_end: date = Field(sa_type=Date(), index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    campus_id: int = Field(foreign_key="campus.id")
    campus: "Campus" = Relationship(back_populates="coverage_per_month")

    coverage: List["Coverage"] = Relationship(back_populates="coverage_per_month")
