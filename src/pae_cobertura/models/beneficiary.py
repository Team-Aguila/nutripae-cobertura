from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .site import Site

class Beneficiary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    last_name: str
    email: str
    phone: str
    address: str
    town: str
    department: str
    postal_code: str
    birth_date: datetime
    gender: str

    site_id: int = Field(foreign_key="site.id")
    site: "Site" = Relationship(back_populates="beneficiaries")
    