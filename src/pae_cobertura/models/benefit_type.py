from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import String, Column

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .coverage import Coverage

class BenefitType(SQLModel, table=True):
    __tablename__ = "benefit_type"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), unique=True, index=True, nullable=False))

    coverages: List["Coverage"] = Relationship(back_populates="benefit_type") 