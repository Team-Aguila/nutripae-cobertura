from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Date
import uuid
from uuid import UUID

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .coveragePerMonth import CoveragePerMonth
    from .beneficiary import Beneficiary

class Coverage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    coverage_per_month_id: UUID = Field(foreign_key="coveragePerMonth.id")
    coverage_per_month: "CoveragePerMonth" = Relationship(back_populates="coverage")

    beneficiary_id: UUID = Field(foreign_key="beneficiary.id")
    beneficiary: "Beneficiary" = Relationship(back_populates="coverage")