from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

class InstitutionBase(SQLModel):
    code: str
    name: str
    main_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    town_id: int

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    main_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    town_id: Optional[int] = None

class InstitutionRead(InstitutionBase):
    id: int

class InstitutionReadWithDetails(InstitutionRead):
    town_name: str
    department_name: str 