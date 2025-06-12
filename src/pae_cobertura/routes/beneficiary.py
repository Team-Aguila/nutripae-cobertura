from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from pae_cobertura.database import get_session
from pae_cobertura.schemas.beneficiary import (
    BeneficiaryCreate,
    BeneficiaryRead,
    BeneficiaryUpdate,
    BeneficiaryReadWithDetails,
)
from pae_cobertura.services.beneficiary import BeneficiaryService

router = APIRouter()

@router.post("/", response_model=BeneficiaryRead)
def create_beneficiary(
    beneficiary_in: BeneficiaryCreate,
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    try:
        return service.create_beneficiary(beneficiary_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{beneficiary_id}", response_model=BeneficiaryReadWithDetails)
def get_beneficiary(
    beneficiary_id: UUID,
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    beneficiary = service.get_beneficiary(beneficiary_id)
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary

@router.get("/", response_model=List[BeneficiaryRead])
def get_beneficiaries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    return service.get_beneficiaries(skip=skip, limit=limit)

@router.put("/{beneficiary_id}", response_model=BeneficiaryRead)
def update_beneficiary(
    beneficiary_id: UUID,
    beneficiary_in: BeneficiaryUpdate,
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    try:
        return service.update_beneficiary(beneficiary_id, beneficiary_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{beneficiary_id}", response_model=BeneficiaryRead)
def patch_beneficiary(
    beneficiary_id: UUID,
    beneficiary_in: BeneficiaryUpdate,
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    try:
        # The service's update method handles partial updates,
        # as the Pydantic model excludes unset values.
        return service.update_beneficiary(beneficiary_id, beneficiary_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{beneficiary_id}")
def delete_beneficiary(
    beneficiary_id: UUID,
    session: Session = Depends(get_session),
):
    service = BeneficiaryService(session)
    try:
        service.delete_beneficiary(beneficiary_id)
        return {"message": "Beneficiary deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 