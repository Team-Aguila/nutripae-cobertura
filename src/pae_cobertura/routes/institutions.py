from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from pae_cobertura.database import engine
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionRead, InstitutionUpdate, InstitutionReadWithDetails
from pae_cobertura.services.institution import (
    create_institution_service,
    get_institution_service,
    get_institutions_service,
    update_institution_service,
    patch_institution_service,
    delete_institution_service
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=InstitutionRead)
def create_institution_endpoint(
    *,
    session: Session = Depends(get_session),
    institution_in: InstitutionCreate
):
    try:
        return create_institution_service(session=session, institution_in=institution_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{institution_id}", response_model=InstitutionReadWithDetails)
def read_institution(
    *,
    session: Session = Depends(get_session),
    institution_id: int
):
    db_institution = get_institution_service(session=session, institution_id=institution_id)
    if not db_institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return db_institution

@router.get("/", response_model=List[InstitutionReadWithDetails])
def read_institutions(
    *,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    return get_institutions_service(session=session, skip=skip, limit=limit)

@router.put("/{institution_id}", response_model=InstitutionRead)
def update_institution_endpoint(
    *,
    session: Session = Depends(get_session),
    institution_id: int,
    institution_in: InstitutionUpdate
):
    try:
        db_institution = update_institution_service(session=session, institution_id=institution_id, institution_in=institution_in)
        if not db_institution:
            raise HTTPException(status_code=404, detail="Institution not found")
        return db_institution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{institution_id}", response_model=InstitutionRead)
def patch_institution_endpoint(
    *,
    session: Session = Depends(get_session),
    institution_id: int,
    institution_in: InstitutionUpdate
):
    try:
        db_institution = patch_institution_service(session=session, institution_id=institution_id, institution_in=institution_in)
        if not db_institution:
            raise HTTPException(status_code=404, detail="Institution not found")
        return db_institution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{institution_id}")
def delete_institution_endpoint(
    *,
    session: Session = Depends(get_session),
    institution_id: int
):
    success = delete_institution_service(session=session, institution_id=institution_id)
    if not success:
        raise HTTPException(status_code=404, detail="Institution not found")
    return {"message": "Institution deleted successfully"}
