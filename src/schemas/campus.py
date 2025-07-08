from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class CampusBase(SQLModel):
    name: str
    dane_code: str
    institution_id: int
    address: str
    latitude: float
    longitude: float

class CampusCreate(CampusBase):
    pass

class CampusUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    institution_id: Optional[int] = None

class CampusResponse(CampusBase):
    id: int
    created_at: datetime
    updated_at: datetime

class CampusResponseWithDetails(CampusResponse):
    number_of_coverages: int
