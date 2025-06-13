from typing import List, Optional
from sqlmodel import Session, select
from pae_cobertura.repositories.campus import CampusRepository
from pae_cobertura.repositories.coverage import CoverageRepository
from pae_cobertura.schemas.campus import CampusCreate, CampusUpdate
from pae_cobertura.models.campus import Campus
from pae_cobertura.models.institution import Institution
from pae_cobertura.models.coverage import Coverage

class CampusService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CampusRepository(session)
        self.coverage_repository = CoverageRepository(session)

    def _validate_institution(self, institution_id: int):
        institution = self.session.get(Institution, institution_id)
        if not institution:
            raise ValueError(f"Institution with id {institution_id} does not exist")

    def create_campus(self, campus_in: CampusCreate) -> dict:
        self._validate_institution(campus_in.institution_id)

        existing_campus_dane_code = self.session.exec(
            select(Campus).where(Campus.dane_code == campus_in.dane_code)
        ).first()
        if existing_campus_dane_code:
            raise ValueError(f"A campus with DANE code {campus_in.dane_code} already exists.")

        existing_campus_name = self.session.exec(
            select(Campus).where(Campus.name == campus_in.name)
        ).first()
        if existing_campus_name:
            raise ValueError(f"A campus with name {campus_in.name} already exists.")

        return self.repository.create(campus_in=campus_in)

    def get_campus(self, campus_id: int) -> Optional[dict]:
        return self.repository.get_by_id(campus_id=campus_id)

    def get_campuses(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_campus(self, campus_id: int, campus_in: CampusUpdate) -> dict:
        db_campus = self.session.get(Campus, campus_id)
        if not db_campus:
            raise ValueError(f"Campus with id {campus_id} not found")

        if campus_in.institution_id is not None:
            self._validate_institution(campus_in.institution_id)

        if campus_in.name is not None:
            existing_campus_name = self.session.exec(
                select(Campus)
                .where(Campus.name == campus_in.name)
                .where(Campus.id != campus_id)
            ).first()
            if existing_campus_name:
                raise ValueError(f"A campus with name {campus_in.name} already exists.")

        if hasattr(campus_in, 'dane_code') and campus_in.dane_code is not None:
            raise ValueError("DANE code cannot be modified once created")

        return self.repository.update(
            db_campus=db_campus,
            campus_in=campus_in
        )

    def delete_campus(self, campus_id: int):
        db_campus = self.session.get(Campus, campus_id)
        if not db_campus:
            raise ValueError(f"Campus with id {campus_id} not found")

        self.repository.delete(db_campus=db_campus)

    def get_coverage_by_campus(self, *, campus_id: int, skip: int = 0, limit: int = 100) -> List[Coverage]:
        db_campus = self.session.get(Campus, campus_id)
        if not db_campus:
            raise ValueError(f"Campus with id {campus_id} not found")

        return self.coverage_repository.get_by_campus(campus_id=campus_id, skip=skip, limit=limit)
