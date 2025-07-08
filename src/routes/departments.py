from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from schemas.departments import DepartmentCreate, DepartmentUpdate, DepartmentResponseWithDetails
from schemas.towns import TownResponseWithDetails as TownResponse
from services.department import DepartmentService
import logging
from core.dependencies import require_create, require_read, require_update, require_delete

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)

@router.post("/", response_model=DepartmentResponseWithDetails)
def create_department(
    department_in: DepartmentCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create()),
):
    logging.info(f"Creating department: {department_in}")
    service = DepartmentService(session)
    try:
        return service.create_department(department_in)
    except ValueError as e:
        logging.error(f"Error creating department: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{department_id}", response_model=DepartmentResponseWithDetails)
def get_department(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting department: {department_id}")
    service = DepartmentService(session)
    department = service.get_department(department_id)
    if not department:
        logging.error(f"Department not found: {department_id}")
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.get("/", response_model=List[dict])
def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting departments: {skip}, {limit}")
    service = DepartmentService(session)
    return service.get_departments(skip=skip, limit=limit)

@router.get("/{department_id}/towns", response_model=List[TownResponse])
def get_department_towns(
    department_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting towns by department: {department_id}, {skip}, {limit}")
    service = DepartmentService(session)
    try:
        return service.get_towns_by_department(department_id=department_id, skip=skip, limit=limit)
    except ValueError as e:
        logging.error(f"Error getting towns by department: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{department_id}", response_model=DepartmentResponseWithDetails)
def update_department(
    department_id: int,
    department_in: DepartmentUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    logging.info(f"Updating department: {department_id}")
    service = DepartmentService(session)
    try:
        return service.update_department(department_id, department_in)
    except ValueError as e:
        logging.error(f"Error updating department: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{department_id}", response_model=DepartmentResponseWithDetails)
def patch_department(
    department_id: int,
    department_in: DepartmentUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    logging.info(f"Patching department: {department_id}")
    service = DepartmentService(session)
    try:
        return service.update_department(department_id, department_in)
    except ValueError as e:
        logging.error(f"Error patching department: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_delete()),
):
    logging.info(f"Deleting department: {department_id}")
    service = DepartmentService(session)
    try:
        service.delete_department(department_id)
        return {"message": "Department deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting department: {e}")
        raise HTTPException(status_code=400, detail=str(e))
