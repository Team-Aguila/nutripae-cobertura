from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, String

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .town import Town
    from .campus import Campus

class Institution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), unique=True, index=True)
    dane_code: str = Field(sa_type=String(13), unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    town_id: int = Field(foreign_key="town.id")
    town: "Town" = Relationship(back_populates="institutions")

    campuses: List["Campus"] = Relationship(back_populates="institution")
