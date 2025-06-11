from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class InstitutionBase(SQLModel):
    name: str
    dane_code: str
    town_id: int

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionUpdate(SQLModel):
    name: Optional[str] = None
    town_id: Optional[int] = None

class InstitutionResponse(InstitutionBase):
    id: int
    created_at: datetime
    updated_at: datetime

class InstitutionResponseWithDetails(InstitutionResponse):
    number_of_campuses: int