from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from schemas.institutions import InstitutionCreate, InstitutionUpdate, InstitutionResponseWithDetails
from schemas.campus import CampusResponseWithDetails as CampusResponse
from services.institution import InstitutionService
import logging
from core.dependencies import require_create, require_read, require_list, require_update, require_delete

router = APIRouter(
    prefix="/institutions",
    tags=["Institutions"],
)

@router.post("/", response_model=InstitutionResponseWithDetails)
def create_institution(
    institution_in: InstitutionCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create()),
):
    logging.info(f"Creating institution: {institution_in}")
    service = InstitutionService(session)
    try:
        return service.create_institution(institution_in)
    except ValueError as e:
        logging.error(f"Error creating institution: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{institution_id}", response_model=InstitutionResponseWithDetails)
def get_institution(
    institution_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting institution: {institution_id}")
    service = InstitutionService(session)
    institution = service.get_institution(institution_id)
    if not institution:
        logging.error(f"Institution not found: {institution_id}")
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution

@router.get("/", response_model=List[InstitutionResponseWithDetails])
def get_institutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    logging.info(f"Getting institutions: {skip}, {limit}")
    service = InstitutionService(session)
    return service.get_institutions(skip=skip, limit=limit)

@router.get("/{institution_id}/campus", response_model=List[CampusResponse])
def get_institution_campus(
    institution_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    logging.info(f"Getting campus by institution: {institution_id}, {skip}, {limit}")
    service = InstitutionService(session)
    try:
        return service.get_campus_by_institution(institution_id=institution_id, skip=skip, limit=limit)
    except ValueError as e:
        logging.error(f"Error getting campus by institution: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{institution_id}", response_model=InstitutionResponseWithDetails)
def update_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    logging.info(f"Updating institution: {institution_id}")
    service = InstitutionService(session)
    try:
        institution = service.update_institution(institution_id, institution_in)
        if not institution:
            logging.error(f"Institution not found: {institution_id}")
            raise HTTPException(status_code=404, detail="Institution not found")
        return institution
    except ValueError as e:
        logging.error(f"Error updating institution: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{institution_id}", response_model=InstitutionResponseWithDetails)
def patch_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    logging.info(f"Patching institution: {institution_id}")
    service = InstitutionService(session)
    try:
        institution = service.update_institution(institution_id, institution_in)
        if not institution:
            logging.error(f"Institution not found: {institution_id}")
            raise HTTPException(status_code=404, detail="Institution not found")
        return institution
    except ValueError as e:
        logging.error(f"Error patching institution: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{institution_id}")
def delete_institution(
    institution_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_delete()),
):
    service = InstitutionService(session)
    try:
        logging.info(f"Deleting institution: {institution_id}")
        service.delete_institution(institution_id)
        return {"message": "Institution deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting institution: {e}")
        raise HTTPException(status_code=400, detail=str(e))
