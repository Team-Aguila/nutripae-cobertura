from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pae_cobertura.database import get_session
from pae_cobertura.schemas.departments import DepartmentCreate, DepartmentUpdate, DepartmentResponseWithDetails
from pae_cobertura.services.department import DepartmentService

router = APIRouter()

@router.post("/", response_model=DepartmentResponseWithDetails)
def create_department(
    department_in: DepartmentCreate,
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    try:
        return service.create_department(department_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{department_id}", response_model=DepartmentResponseWithDetails)
def get_department(
    department_id: int,
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    department = service.get_department(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.get("/", response_model=List[dict])
def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    return service.get_departments(skip=skip, limit=limit)

@router.put("/{department_id}", response_model=DepartmentResponseWithDetails)
def update_department(
    department_id: int,
    department_in: DepartmentUpdate,
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    try:
        return service.update_department(department_id, department_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{department_id}", response_model=DepartmentResponseWithDetails)
def patch_department(
    department_id: int,
    department_in: DepartmentUpdate,
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    try:
        return service.update_department(department_id, department_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    session: Session = Depends(get_session)
):
    service = DepartmentService(session)
    try:
        service.delete_department(department_id)
        return {"message": "Department deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 