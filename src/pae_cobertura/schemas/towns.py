from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class TownBase(SQLModel):
    name: str
    dane_code: str
    department_id: int

class TownCreate(TownBase):
    pass

class TownUpdate(SQLModel):
    name: Optional[str] = None
    department_id: Optional[int] = None

class TownResponse(TownBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TownResponseWithDetails(TownResponse):
    number_of_institutions: int 