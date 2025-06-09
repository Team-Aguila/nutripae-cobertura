# pae_cobertura/schemas/departments.py
from typing import Optional
from sqlmodel import SQLModel

# Schema para la creación (no incluye ID)
class DepartmentCreate(SQLModel):
    code: str
    name: str

# Schema para la actualización (todos los campos son opcionales)
class DepartmentUpdate(SQLModel):
    name: Optional[str] = None

# Schema para la lectura (incluye ID y campos calculados)
class DepartmentRead(DepartmentCreate):
    id: int

# Schema para la lectura con detalles (incluye el número de municipios)
class DepartmentReadWithDetails(DepartmentRead):
    number_of_towns: int