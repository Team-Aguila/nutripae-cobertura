from typing import List, Optional
from sqlmodel import Session, select
from repositories.institution import InstitutionRepository
from repositories.campus import CampusRepository
from schemas.institutions import InstitutionCreate, InstitutionUpdate
from models.institution import Institution
from models.town import Town
import logging

class InstitutionService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = InstitutionRepository(session)
        self.campus_repository = CampusRepository(session)

    def _validate_town(self, town_id: int):
        town = self.session.get(Town, town_id)
        if not town:
            logging.error(f"Town with id {town_id} does not exist")
            raise ValueError(f"Town with id {town_id} does not exist")

    def create_institution(self, institution_in: InstitutionCreate) -> dict:
        logging.info(f"Creating institution: {institution_in}")
        existing_institution_with_dane_code = self.session.exec(
            select(Institution).where(Institution.dane_code == institution_in.dane_code)
        ).first()
        existing_institution_with_name = self.session.exec(
            select(Institution).where(Institution.name == institution_in.name)
        ).first()

        if existing_institution_with_dane_code:
            logging.error(f"An institution with DANE code {institution_in.dane_code} already exists.")
            raise ValueError(f"An institution with DANE code {institution_in.dane_code} already exists.")

        if existing_institution_with_name:
            logging.error(f"An institution with name {institution_in.name} already exists.")
            raise ValueError(f"An institution with name {institution_in.name} already exists.")

        self._validate_town(institution_in.town_id)

        return self.repository.create(institution_in=institution_in)

    def get_institution(self, institution_id: int) -> Optional[dict]:
        logging.info(f"Getting institution: {institution_id}")
        return self.repository.get_by_id(institution_id=institution_id)

    def get_institutions(self, skip: int = 0, limit: int = 100) -> List[dict]:
        logging.info(f"Getting institutions: {skip}, {limit}")
        return self.repository.get_all(skip=skip, limit=limit)

    def update_institution(self, institution_id: int, institution_in: InstitutionUpdate) -> dict:
        logging.info(f"Updating institution: {institution_id}")
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            logging.error(f"Institution with id {institution_id} not found")
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
                logging.error(f"An institution with name {institution_in.name} already exists.")
                raise ValueError(f"An institution with name {institution_in.name} already exists.")

        if hasattr(institution_in, 'dane_code') and institution_in.dane_code is not None:
            logging.error("DANE code cannot be modified once created")
            raise ValueError("DANE code cannot be modified once created")

        return self.repository.update(
            db_institution=db_institution,
            institution_in=institution_in
        )

    def delete_institution(self, institution_id: int):
        logging.info(f"Deleting institution: {institution_id}")
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            logging.error(f"Institution with id {institution_id} not found")
            raise ValueError(f"Institution with id {institution_id} not found")

        self.repository.delete(db_institution=db_institution)

    def get_campus_by_institution(self, *, institution_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        logging.info(f"Getting campus by institution: {institution_id}, {skip}, {limit}")
        db_institution = self.session.get(Institution, institution_id)
        if not db_institution:
            logging.error(f"Institution with id {institution_id} not found")
            raise ValueError(f"Institution with id {institution_id} not found")

        return self.campus_repository.get_by_institution(institution_id=institution_id, skip=skip, limit=limit)
