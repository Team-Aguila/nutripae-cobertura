# pae_cobertura/api/endpoints/departamentos.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from pae_cobertura.database import engine
from pae_cobertura.schemas.departments import DepartmentCreate, DepartmentRead, DepartmentUpdate, DepartmentReadWithDetails
from pae_cobertura.models.department import Department
from pae_cobertura.repositories.department import create_department, get_department_by_id, get_all_departments, update_department, delete_department

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=DepartmentRead)
def create_department_route(*, session: Session = Depends(get_session), department_in: DepartmentCreate):
    """
    Registrar un nuevo departamento.
    """
    # Aquí podrías añadir una validación para ver si el código DANE o nombre ya existen
    # y lanzar un HTTPException(409, "Conflicto, el recurso ya existe")
    return create_department(session=session, department_in=department_in)

@router.get("/", response_model=List[DepartmentReadWithDetails])
def get_all_departments_route(
    *,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200)
):
    """
    Consultar todos los departamentos con paginación.
    """
    return get_all_departments(session=session, skip=skip, limit=limit)

@router.get("/{department_id}", response_model=DepartmentRead)
def get_department_by_id_route(*, session: Session = Depends(get_session), department_id: int):
    """
    Consultar un departamento por su ID.
    """
    db_department = get_department_by_id(session=session, department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.patch("/{department_id}", response_model=DepartmentRead)
def update_department_route(
    *,
    session: Session = Depends(get_session),
    department_id: int,
    department_in: DepartmentUpdate
):
    """
    Modificar un departamento existente. El código DANE no es editable.
    """
    db_department = get_department_by_id(session=session, department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return update_department(
        session=session, db_department=db_department, department_in=department_in
    )

@router.delete("/{department_id}", status_code=204)
def delete_department_route(*, session: Session = Depends(get_session), department_id: int):
    """
    Eliminar un departamento. No se permite si tiene municipios asociados.
    """
    db_department = get_department_by_id(session=session, department_id=department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")

    if db_department.towns:
        raise HTTPException(
            status_code=409, # Conflict
            detail="Cannot delete department because it has towns associated."
        )

    delete_department(session=session, db_department=db_department)
    return None # Return a 204 No Content
