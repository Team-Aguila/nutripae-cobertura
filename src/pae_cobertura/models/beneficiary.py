from typing import List, Optional
from datetime import datetime, date
from sqlmodel import Field, Relationship, SQLModel, String
import uuid
from uuid import UUID
from sqlalchemy import Boolean, Integer, Date

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .campus import Campus
    from .coverage import Coverage
    from .document_type import DocumentType
    from .gender import Gender
    from .grade import Grade
    from .etnic_group import EtnicGroup
    from .disability_type import DisabilityType

class Beneficiary(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    year: int = Field(sa_type=Integer, index=True)

    document_type_id: int = Field(foreign_key="document_type.id", nullable=False)
    document_type: "DocumentType" = Relationship(back_populates="beneficiaries")

    number_document: str = Field(sa_type=String(20),unique=True, index=True)
    first_name: str = Field(sa_type=String(50), index=True, nullable=False)
    second_name: Optional[str] = Field(sa_type=String(50), default=None)
    first_surname: str = Field(sa_type=String(50), index=True, nullable=False)
    second_surname: Optional[str] = Field(sa_type=String(50), default=None)
    birth_date: date = Field(sa_type=Date(), index=True)

    gender_id: int = Field(foreign_key="gender.id", nullable=False)
    gender: "Gender" = Relationship(back_populates="beneficiaries")

    grade_id: int = Field(foreign_key="grade.id", nullable=False)
    grade: "Grade" = Relationship(back_populates="beneficiaries")

    etnic_group_id: Optional[int] = Field(foreign_key="etnic_group.id")
    etnic_group: Optional["EtnicGroup"] = Relationship(back_populates="beneficiaries")

    victim_conflict: Optional[bool] = Field(sa_type=Boolean, default=False)

    disability_type_id: Optional[int] = Field(foreign_key="disability_type.id")
    disability_type: Optional["DisabilityType"] = Relationship(back_populates="beneficiaries")

    attendant_number: Optional[int] = Field(sa_type=Integer, default=1)
    attendant_name: Optional[str] = Field(sa_type=String(50), default=None)
    attendant_phone: Optional[str] = Field(sa_type=String(20), default=None)
    attendant_relationship: Optional[str] = Field(sa_type=String(50), default=None)

    retirement_date: Optional[date] = Field(sa_type=Date())
    retirement_reason: Optional[str] = Field(sa_type=String(255), default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    coverage: List["Coverage"] = Relationship(back_populates="beneficiary")
