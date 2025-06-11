from typing import List, Optional
from datetime import datetime, date
from sqlmodel import Field, Relationship, SQLModel, String
import uuid
from uuid import UUID
from sqlalchemy import Boolean, Integer, Enum, Date
from enum import Enum as PyEnum

# Para evitar error de "circular import" con las relaciones
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .campus import Campus
    from .coverage import Coverage

class DocumentType(str, PyEnum):
    BIRTH_CERTIFICATE = "registro de nacimiento"
    ID_CARD = "documento de identidad"
    PASSPORT = "pasaporte"
    FOREIGN_ID = "documento extranjero"

class Gender(str, PyEnum):
    MALE = "masculino"
    FEMALE = "femenino"
    OTHER = "otro"

class Grade(str, PyEnum):
    # Educación Inicial
    INITIAL_0_1 = "inicial 0-1 años"
    INITIAL_1_2 = "inicial 1-2 años"
    INITIAL_2_3 = "inicial 2-3 años"
    
    # Educación Preescolar
    PRE_JARDIN = "pre-jardín"
    JARDIN = "jardín"
    TRANSICION = "transición"
    
    # Educación Básica Primaria
    PRIMERO = "primero"
    SEGUNDO = "segundo"
    TERCERO = "tercero"
    CUARTO = "cuarto"
    QUINTO = "quinto"
    
    # Educación Básica Secundaria
    SEXTO = "sexto"
    SEPTIMO = "séptimo"
    OCTAVO = "octavo"
    NOVENO = "noveno"
    
    # Educación Media
    DECIMO = "décimo"
    ONCE = "once"

class EtnicGroup(str, PyEnum):
    AFRICAN = "afro"
    AMERICAN = "indígena"
    ASIAN = "palenquero"
    EUROPEAN = "rom"
    MIXED = "mestizo"
    OTHER = "otro"
    INDIGENOUS = "indígena"

class DisabilityType(str, PyEnum):
    VISUAL = "visual"
    AUDITIVO = "auditiva"
    MOTORA = "motora"
    INTELECTUAL = "intelectual"
    MULTIPLE = "multiple"

class Beneficiary(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    year: int = Field(sa_type=Integer, index=True)
    type_document: DocumentType = Field(sa_type=Enum(DocumentType), index=True, nullable=False)
    number_document: str = Field(sa_type=String(20), index=True)
    first_name: str = Field(sa_type=String(50), index=True, nullable=False)
    second_name: str = Field(sa_type=String(50))
    first_surname: str = Field(sa_type=String(50), index=True, nullable=False)
    second_surname: str = Field(sa_type=String(50))
    birth_date: date = Field(sa_type=Date(), index=True)
    gender: Gender = Field(sa_type=Enum(Gender), index=True, nullable=False)
    grade: Grade = Field(sa_type=Enum(Grade), nullable=False)
    etnic_group: Optional[EtnicGroup] = Field(sa_type=Enum(EtnicGroup), nullable=True)
    victim_conflict: bool = Field(sa_type=Boolean, default=False)
    disability_type: Optional[DisabilityType] = Field(sa_type=Enum(DisabilityType), nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    coverage: List["Coverage"] = Relationship(back_populates="beneficiary")
