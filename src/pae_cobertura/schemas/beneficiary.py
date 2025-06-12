from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel

from pae_cobertura.models.document_type import DocumentType
from pae_cobertura.models.gender import Gender
from pae_cobertura.models.grade import Grade
from pae_cobertura.models.etnic_group import EtnicGroup
from pae_cobertura.models.disability_type import DisabilityType
from pae_cobertura.models.coverage import Coverage


class BeneficiaryBase(SQLModel):
    year: int
    document_type_id: int
    number_document: str
    first_name: str
    second_name: Optional[str] = None
    first_surname: str
    second_surname: Optional[str] = None
    birth_date: date
    gender_id: int
    grade_id: int
    etnic_group_id: Optional[int] = None
    victim_conflict: Optional[bool] = False
    disability_type_id: Optional[int] = None
    attendant_number: Optional[int] = 1
    attendant_name: Optional[str] = None
    attendant_phone: Optional[str] = None
    attendant_relationship: Optional[str] = None
    retirement_date: Optional[date] = None
    retirement_reason: Optional[str] = None


class BeneficiaryCreate(BeneficiaryBase):
    pass


class BeneficiaryUpdate(SQLModel):
    year: Optional[int] = None
    document_type_id: Optional[int] = None
    number_document: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    birth_date: Optional[date] = None
    gender_id: Optional[int] = None
    grade_id: Optional[int] = None
    etnic_group_id: Optional[int] = None
    victim_conflict: Optional[bool] = None
    disability_type_id: Optional[int] = None
    attendant_number: Optional[int] = None
    attendant_name: Optional[str] = None
    attendant_phone: Optional[str] = None
    attendant_relationship: Optional[str] = None
    retirement_date: Optional[date] = None
    retirement_reason: Optional[str] = None


class BeneficiaryRead(BeneficiaryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class BeneficiaryReadWithDetails(BeneficiaryRead):
    document_type: Optional[DocumentType] = None
    gender: Optional[Gender] = None
    grade: Optional[Grade] = None
    etnic_group: Optional[EtnicGroup] = None
    disability_type: Optional[DisabilityType] = None
    coverage: List[Coverage] = []

    class Config:
        from_attributes = True
