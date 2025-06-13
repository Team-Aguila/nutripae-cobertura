from typing import List, Optional
from sqlmodel import Session, select
from pae_cobertura.repositories.town import TownRepository
from pae_cobertura.repositories.institution import InstitutionRepository
from pae_cobertura.schemas.towns import TownCreate, TownUpdate
from pae_cobertura.models.town import Town
from pae_cobertura.models.department import Department

class TownService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = TownRepository(session)
        self.institution_repository = InstitutionRepository(session)

    def _validate_department(self, department_id: int):
        department = self.session.get(Department, department_id)
        if not department:
            raise ValueError(f"Department with id {department_id} does not exist")

    def create_town(self, town_in: TownCreate) -> dict:
        existing_town_with_dane_code = self.session.exec(
            select(Town).where(Town.dane_code == town_in.dane_code)
        ).first()
        existing_town_with_name = self.session.exec(
            select(Town).where(Town.name == town_in.name)
        ).first()

        if existing_town_with_dane_code:
            raise ValueError(f"A town with DANE code {town_in.dane_code} already exists.")

        if existing_town_with_name:
            raise ValueError(f"A town with name {town_in.name} already exists.")

        self._validate_department(town_in.department_id)

        return self.repository.create(town_in=town_in)

    def get_town(self, town_id: int) -> Optional[dict]:
        return self.repository.get_by_id(town_id=town_id)

    def get_towns(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_town(self, town_id: int, town_in: TownUpdate) -> dict:
        db_town = self.session.get(Town, town_id)
        if not db_town:
            raise ValueError(f"Town with id {town_id} not found")

        if town_in.department_id is not None:
            self._validate_department(town_in.department_id)

        if town_in.name is not None:
            existing_town_with_name = self.session.exec(
                select(Town)
                .where(Town.name == town_in.name)
                .where(Town.id != town_id)
            ).first()
            if existing_town_with_name:
                raise ValueError(f"A town with name {town_in.name} already exists.")

        if hasattr(town_in, 'dane_code') and town_in.dane_code is not None:
            raise ValueError("DANE code cannot be modified once created")

        return self.repository.update(
            db_town=db_town,
            town_in=town_in
        )

    def delete_town(self, town_id: int):
        db_town = self.session.get(Town, town_id)
        if not db_town:
            raise ValueError(f"Town with id {town_id} not found")

        self.repository.delete(db_town=db_town)

    def get_institutions_by_town(self, *, town_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        db_town = self.session.get(Town, town_id)
        if not db_town:
            raise ValueError(f"Town with id {town_id} not found")

        return self.institution_repository.get_by_town(town_id=town_id, skip=skip, limit=limit)
