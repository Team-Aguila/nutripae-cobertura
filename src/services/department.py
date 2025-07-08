from typing import List, Optional
from sqlmodel import Session, select
from repositories.department import DepartmentRepository
from repositories.town import TownRepository
from schemas.departments import DepartmentCreate, DepartmentUpdate
from models.department import Department
import logging

class DepartmentService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = DepartmentRepository(session)
        self.town_repository = TownRepository(session)

    def create_department(self, department_in: DepartmentCreate) -> Department:
        logging.info(f"Creating department: {department_in}")
        existing_department_with_dane_code = self.session.exec(
            select(Department).where(Department.dane_code == department_in.dane_code)
        ).first()
        existing_department_with_name = self.session.exec(
            select(Department).where(Department.name == department_in.name)
        ).first()

        if existing_department_with_dane_code:
            logging.error(f"A department with DANE code {department_in.dane_code} already exists.")
            raise ValueError(f"A department with DANE code {department_in.dane_code} already exists.")

        if existing_department_with_name:
            logging.error(f"A department with name {department_in.name} already exists.")
            raise ValueError(f"A department with name {department_in.name} already exists.")

        return self.repository.create(department_in=department_in)

    def get_department(self, department_id: int) -> Optional[Department]:
        logging.info(f"Getting department: {department_id}")
        return self.repository.get_by_id(department_id=department_id)

    def get_departments(self, skip: int = 0, limit: int = 100) -> List[dict]:
        logging.info(f"Getting departments: {skip}, {limit}")
        return self.repository.get_all(skip=skip, limit=limit)

    def update_department(self, department_id: int, department_in: DepartmentUpdate) -> Department:
        logging.info(f"Updating department: {department_id}")
        db_department = self.session.get(Department, department_id)
        if not db_department:
            logging.error(f"Department with id {department_id} not found")
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
        logging.info(f"Deleting department: {department_id}")
        db_department = self.session.get(Department, department_id)
        if not db_department:
            logging.error(f"Department with id {department_id} not found")
            raise ValueError(f"Department with id {department_id} not found")

        self.repository.delete(db_department=db_department)

    def get_towns_by_department(self, *, department_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        logging.info(f"Getting towns by department: {department_id}, {skip}, {limit}")
        db_department = self.session.get(Department, department_id)
        if not db_department:
            logging.error(f"Department with id {department_id} not found")
            raise ValueError(f"Department with id {department_id} not found")

        return self.town_repository.get_by_department(department_id=department_id, skip=skip, limit=limit)
