from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Date
import uuid
from uuid import UUID

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .campus import Campus
    from .beneficiary import Beneficiary
    from .benefit_type import BenefitType

class Coverage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    benefit_type_id: int = Field(foreign_key="benefit_type.id", nullable=False)
    benefit_type: "BenefitType" = Relationship(back_populates="coverages")

    campus_id: int = Field(foreign_key="campus.id")
    campus: "Campus" = Relationship(back_populates="coverage")

    beneficiary_id: UUID = Field(foreign_key="beneficiary.id")
    beneficiary: "Beneficiary" = Relationship(back_populates="coverage")
