from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import String, Column

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .beneficiary import Beneficiary

class EtnicGroup(SQLModel, table=True):
    __tablename__ = "etnic_group"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), unique=True, index=True, nullable=False))

    beneficiaries: List["Beneficiary"] = Relationship(back_populates="etnic_group")
