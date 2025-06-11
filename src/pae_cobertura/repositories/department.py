from datetime import datetime
from sqlmodel import Session, select, func
from pae_cobertura.models.department import Department
from pae_cobertura.models.town import Town
from pae_cobertura.schemas.departments import DepartmentCreate, DepartmentUpdate

class DepartmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, department_in: DepartmentCreate) -> dict:
        db_department = Department.model_validate(department_in)
        self.session.add(db_department)
        self.session.commit()
        self.session.refresh(db_department)
        
        department_dict = db_department.model_dump()
        department_dict["number_of_towns"] = 0
        
        return department_dict

    def get_by_id(self, *, department_id: int) -> dict | None:
        department = self.session.get(Department, department_id)
        if not department:
            return None
            
        statement = (
            select(func.count(Town.id))
            .where(Town.department_id == department_id)
        )
        town_count = self.session.exec(statement).first()
        
        department_dict = department.model_dump()
        department_dict["number_of_towns"] = town_count or 0
        
        return department_dict

    def get_all(self, *, skip: int = 0, limit: int = 100) -> list[dict]:
        town_count = (
            select(
                Town.department_id,
                func.count(Town.id).label("town_count")
            )
            .group_by(Town.department_id)
            .subquery()
        )
        
        statement = (
            select(
                Department.id,
                Department.dane_code,
                Department.name,
                Department.created_at,
                Department.updated_at,
                func.coalesce(town_count.c.town_count, 0).label("number_of_towns")
            )
            .outerjoin(town_count, Department.id == town_count.c.department_id)
            .order_by(Department.name)
            .offset(skip)
            .limit(limit)
        )
        
        result = self.session.exec(statement).mappings().all()
        return result

    def update(self, *, db_department: Department, department_in: DepartmentUpdate) -> dict:
        update_data = department_in.model_dump(exclude_unset=True)
        if 'dane_code' in update_data:
            del update_data['dane_code']
        
        for key, value in update_data.items():
            setattr(db_department, key, value)
        
        db_department.updated_at = datetime.now()
        self.session.add(db_department)
        self.session.commit()
        self.session.refresh(db_department)
        
        statement = (
            select(func.count(Town.id))
            .where(Town.department_id == db_department.id)
        )
        town_count = self.session.exec(statement).first()
        
        department_dict = db_department.model_dump()
        department_dict["number_of_towns"] = town_count or 0
        
        return department_dict

    def delete(self, *, db_department: Department):
        statement = select(func.count(Town.id)).where(Town.department_id == db_department.id)
        town_count = self.session.exec(statement).first()
        
        if town_count > 0:
            raise ValueError(f"No se puede eliminar el departamento {db_department.name} porque tiene {town_count} municipios asociados")
        
        self.session.delete(db_department)
        self.session.commit()
