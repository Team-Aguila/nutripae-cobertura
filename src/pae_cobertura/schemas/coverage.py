from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel

class CoverageBase(SQLModel):
    active: bool = True
    benefit_type_id: int
    campus_id: int
    beneficiary_id: UUID

class CoverageCreate(CoverageBase):
    pass

class CoverageUpdate(SQLModel):
    active: Optional[bool] = None
    benefit_type_id: Optional[int] = None
    campus_id: Optional[int] = None
    beneficiary_id: Optional[UUID] = None

class CoverageRead(CoverageBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class CoverageReadWithDetails(CoverageRead):
    # If relationships need to be shown, they would be defined here.
    # benefit_type: Optional["BenefitType"] = None
    # campus: Optional["Campus"] = None
    # beneficiary: Optional["Beneficiary"] = None
    pass

    class Config:
        from_attributes = True
