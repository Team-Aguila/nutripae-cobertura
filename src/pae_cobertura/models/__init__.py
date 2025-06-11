# pae_cobertura/models/__init__.py
from sqlmodel import SQLModel

from .department import Department
from .town import Town
from .institution import Institution
from .campus import Campus
from .beneficiary import Beneficiary
from .coverage import Coverage
from .document_type import DocumentType
from .gender import Gender
from .grade import Grade
from .etnic_group import EtnicGroup
from .disability_type import DisabilityType
from .benefit_type import BenefitType
