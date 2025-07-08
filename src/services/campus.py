from typing import List, Optional
from sqlmodel import Session, select
from repositories.campus import CampusRepository
from repositories.coverage import CoverageRepository
from schemas.campus import CampusCreate, CampusUpdate
from models.campus import Campus
from models.institution import Institution
from models.coverage import Coverage
import logging

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
        logging.info(f"Creating campus: {campus_in}")
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
        logging.info(f"Getting campus: {campus_id}")
        return self.repository.get_by_id(campus_id=campus_id)

    def get_campuses(self, skip: int = 0, limit: int = 100) -> List[dict]:
        logging.info(f"Getting campuses: {skip}, {limit}")
        return self.repository.get_all(skip=skip, limit=limit)

    def update_campus(self, campus_id: int, campus_in: CampusUpdate) -> dict:
        logging.info(f"Updating campus: {campus_id}")
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
        logging.info(f"Deleting campus: {campus_id}")
        db_campus = self.session.get(Campus, campus_id)
        if not db_campus:
            raise ValueError(f"Campus with id {campus_id} not found")

        self.repository.delete(db_campus=db_campus)

    def get_coverage_by_campus(self, *, campus_id: int, skip: int = 0, limit: int = 100) -> List[Coverage]:
        logging.info(f"Getting coverage by campus: {campus_id}, {skip}, {limit}")
        db_campus = self.session.get(Campus, campus_id)
        if not db_campus:
            raise ValueError(f"Campus with id {campus_id} not found")

        return self.coverage_repository.get_by_campus(campus_id=campus_id, skip=skip, limit=limit)
