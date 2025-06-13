from typing import List, Optional
from sqlmodel import Session, select
from pae_cobertura.repositories.department import DepartmentRepository
from pae_cobertura.repositories.town import TownRepository
from pae_cobertura.schemas.departments import DepartmentCreate, DepartmentUpdate
from pae_cobertura.models.department import Department

class DepartmentService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = DepartmentRepository(session)
        self.town_repository = TownRepository(session)

    def create_department(self, department_in: DepartmentCreate) -> Department:
        existing_department_with_dane_code = self.session.exec(
            select(Department).where(Department.dane_code == department_in.dane_code)
        ).first()
        existing_department_with_name = self.session.exec(
            select(Department).where(Department.name == department_in.name)
        ).first()

        if existing_department_with_dane_code:
            raise ValueError(f"A department with DANE code {department_in.dane_code} already exists.")

        if existing_department_with_name:
            raise ValueError(f"A department with name {department_in.name} already exists.")

        return self.repository.create(department_in=department_in)

    def get_department(self, department_id: int) -> Optional[Department]:
        return self.repository.get_by_id(department_id=department_id)

    def get_departments(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_department(self, department_id: int, department_in: DepartmentUpdate) -> Department:
        db_department = self.session.get(Department, department_id)
        if not db_department:
            raise ValueError(f"Department with id {department_id} not found")

        if department_in.name is not None:
            existing_department_with_name = self.session.exec(
                select(Department)
                .where(Department.name == department_in.name)
                .where(Department.id != department_id)
            ).first()
            if existing_department_with_name:
                raise ValueError(f"A department with name {department_in.name} already exists.")

        if hasattr(department_in, 'dane_code') and department_in.dane_code is not None:
            raise ValueError("DANE code cannot be modified once created")

        return self.repository.update(
            db_department=db_department,
            department_in=department_in
        )

    def delete_department(self, department_id: int) -> None:
        db_department = self.session.get(Department, department_id)
        if not db_department:
            raise ValueError(f"Department with id {department_id} not found")

        self.repository.delete(db_department=db_department)

    def get_towns_by_department(self, *, department_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        db_department = self.session.get(Department, department_id)
        if not db_department:
            raise ValueError(f"Department with id {department_id} not found")

        return self.town_repository.get_by_department(department_id=department_id, skip=skip, limit=limit)
