from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .institution import Institucion
    from .beneficiary import Beneficiary

class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name: str
    address: str
    latitude: float
    longitude: float

    institution_id: int = Field(foreign_key="institution.id")
    institution: "Institucion" = Relationship(back_populates="sites")
    
    beneficiaries: List["Beneficiary"] = Relationship(back_populates="site")