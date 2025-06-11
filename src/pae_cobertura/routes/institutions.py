from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pae_cobertura.database import get_session
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionUpdate, InstitutionResponseWithDetails
from pae_cobertura.services.institution import InstitutionService

router = APIRouter()

@router.post("/", response_model=InstitutionResponseWithDetails)
def create_institution(
    institution_in: InstitutionCreate,
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    try:
        return service.create_institution(institution_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{institution_id}", response_model=InstitutionResponseWithDetails)
def get_institution(
    institution_id: int,
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    institution = service.get_institution(institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution

@router.get("/", response_model=List[InstitutionResponseWithDetails])
def get_institutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    return service.get_institutions(skip=skip, limit=limit)

@router.put("/{institution_id}", response_model=InstitutionResponseWithDetails)
def update_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    try:
        institution = service.update_institution(institution_id, institution_in)
        if not institution:
            raise HTTPException(status_code=404, detail="Institution not found")
        return institution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{institution_id}", response_model=InstitutionResponseWithDetails)
def patch_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    try:
        institution = service.update_institution(institution_id, institution_in)
        if not institution:
            raise HTTPException(status_code=404, detail="Institution not found")
        return institution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{institution_id}")
def delete_institution(
    institution_id: int,
    session: Session = Depends(get_session)
):
    service = InstitutionService(session)
    try:
        service.delete_institution(institution_id)
        return {"message": "Institution deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
