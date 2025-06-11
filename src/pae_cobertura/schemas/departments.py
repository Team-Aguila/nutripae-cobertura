# pae_cobertura/schemas/departments.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

# Schema para la creación (no incluye ID)
class DepartmentCreate(SQLModel):
    dane_code: str
    name: str

# Schema para la actualización (todos los campos son opcionales)
class DepartmentUpdate(SQLModel):
    name: Optional[str] = None

# Schema base para respuestas
class DepartmentBase(SQLModel):
    id: int
    dane_code: str
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# Schema para la respuesta básica
class DepartmentResponse(DepartmentBase):
    pass

# Schema para la respuesta con detalles (incluye el número de municipios)
class DepartmentResponseWithDetails(DepartmentBase):
    number_of_towns: int
