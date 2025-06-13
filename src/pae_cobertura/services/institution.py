from typing import List, Optional
from sqlmodel import Session, select
from pae_cobertura.repositories.institution import InstitutionRepository
from pae_cobertura.repositories.campus import CampusRepository
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionUpdate
from pae_cobertura.models.institution import Institution
from pae_cobertura.models.town import Town

class InstitutionService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = InstitutionRepository(session)
        self.campus_repository = CampusRepository(session)

    def _validate_town(self, town_id: int):
        town = self.session.get(Town, town_id)
        if not town:
            raise ValueError(f"Town with id {town_id} does not exist")

    def create_institution(self, institution_in: InstitutionCreate) -> dict:
        existing_institution_with_dane_code = self.session.exec(
            select(Institution).where(Institution.dane_code == institution_in.dane_code)
        ).first()
        existing_institution_with_name = self.session.exec(
            select(Institution).where(Institution.name == institution_in.name)
        ).first()

        if existing_institution_with_dane_code:
            raise ValueError(f"An institution with DANE code {institution_in.dane_code} already exists.")

        if existing_institution_with_name:
            raise ValueError(f"An institution with name {institution_in.name} already exists.")

        self._validate_town(institution_in.town_id)

        return self.repository.create(institution_in=institution_in)

    def get_institution(self, institution_id: int) -> Optional[dict]:
        return self.repository.get_by_id(institution_id=institution_id)

    def get_institutions(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_institution(self, institution_id: int, institution_in: InstitutionUpdate) -> dict:
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            raise ValueError(f"Institution with id {institution_id} not found")

        if institution_in.town_id is not None:
            self._validate_town(institution_in.town_id)

        if institution_in.name is not None:
            existing_institution_with_name = self.session.exec(
                select(Institution)
                .where(Institution.name == institution_in.name)
                .where(Institution.id != institution_id)
            ).first()
            if existing_institution_with_name:
                raise ValueError(f"An institution with name {institution_in.name} already exists.")

        if hasattr(institution_in, 'dane_code') and institution_in.dane_code is not None:
            raise ValueError("DANE code cannot be modified once created")

        return self.repository.update(
            db_institution=db_institution,
            institution_in=institution_in
        )

    def delete_institution(self, institution_id: int):
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            raise ValueError(f"Institution with id {institution_id} not found")

        self.repository.delete(db_institution=db_institution)

    def get_campus_by_institution(self, *, institution_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            raise ValueError(f"Institution with id {institution_id} not found")

        return self.campus_repository.get_by_institution(institution_id=institution_id, skip=skip, limit=limit)
