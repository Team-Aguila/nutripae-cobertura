# pae_cobertura/crud/crud_departamento.py
from sqlmodel import Session, select, func
from pae_cobertura.models.department import Department
from pae_cobertura.models.town import Town
from pae_cobertura.schemas.departments import DepartmentCreate, DepartmentUpdate

def create_department(*, session: Session, department_in: DepartmentCreate) -> Department:
    # Crea una instancia del modelo de BD a partir del schema
    db_department = Department.model_validate(department_in)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department

def get_department_by_id(*, session: Session, department_id: int) -> Department | None:
    return session.get(Department, department_id)

def get_all_departments(*, session: Session, skip: int = 0, limit: int = 100) -> list[dict]:
    # Esta consulta es más compleja para incluir el conteo de municipios
    statement = (
        select(
            Department.id,
            Department.code,
            Department.name,
            func.count(Town.id).label("number_of_towns")
        )
        .outerjoin(Town, Department.id == Town.department_id)
        .group_by(Department.id)
        .offset(skip)
        .limit(limit)
    )
    result = session.exec(statement).mappings().all()
    return result

def update_department(*, session: Session, db_department: Department, department_in: DepartmentUpdate) -> Department:
    update_data = department_in.model_dump(exclude_unset=True)
    db_department.sqlmodel_update(update_data)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department

def delete_department(*, session: Session, db_department: Department):
    session.delete(db_department)
    session.commit()
    # No se retorna nada tras la eliminación