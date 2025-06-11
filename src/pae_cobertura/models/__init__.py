# pae_cobertura/models/__init__.py
from sqlmodel import SQLModel

from .department import Department
from .town import Town
from .institution import Institution
from .campus import Campus
from .beneficiary import Beneficiary
from .coveragePerMonth import CoveragePerMonth
from .coverage import Coverage
