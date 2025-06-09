from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .town import Town

class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(sa_type=String(2), unique=True, index=True)
    name: str = Field(unique=True, index=True)

    towns: List["Town"] = Relationship(back_populates="department")
