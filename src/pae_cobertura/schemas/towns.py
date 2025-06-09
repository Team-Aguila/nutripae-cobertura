from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel

class TownBase(SQLModel):
    code: str
    name: str
    department_id: int

class TownCreate(TownBase):
    pass

class TownUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    department_id: Optional[int] = None

class TownRead(TownBase):
    id: int

class TownReadWithDetails(TownRead):
    department_name: str 