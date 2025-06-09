from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .department import Department
    from .institution import Institution

class Town(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_dane: str = Field(sa_type=String(3), index=True)
    name: str = Field(index=True)

    department_id: int = Field(foreign_key="department.id")
    department: "Department" = Relationship(back_populates="towns")

    institutions: List["Institution"] = Relationship(back_populates="town")
