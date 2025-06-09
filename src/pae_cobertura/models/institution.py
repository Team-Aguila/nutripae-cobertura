from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .town import Town
    from .site import Site

class Institution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name: str
    main_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

    town_id: int = Field(foreign_key="town.id")
    town: "Town" = Relationship(back_populates="institutions")

    sites: List["Site"] = Relationship(back_populates="institution")