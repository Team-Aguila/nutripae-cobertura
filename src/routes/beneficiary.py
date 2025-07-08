from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from database import get_session
from schemas.beneficiary import (
    BeneficiaryCreate,
    BeneficiaryRead,
    BeneficiaryUpdate,
    BeneficiaryReadWithDetails,
)
from services.beneficiary import BeneficiaryService
import logging
from core.dependencies import require_create, require_read, require_update, require_delete, require_list

router = APIRouter(
    prefix="/beneficiaries",
    tags=["Beneficiaries"],
)

@router.post("/", response_model=BeneficiaryRead)
def create_beneficiary(
    beneficiary_in: BeneficiaryCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create()),
):
    service = BeneficiaryService(session)
    try:
        logging.info(f"Creating beneficiary: {beneficiary_in}")
        return service.create_beneficiary(beneficiary_in)
    except ValueError as e:
        logging.error(f"Error creating beneficiary: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{beneficiary_id}", response_model=BeneficiaryReadWithDetails)
def get_beneficiary(
    beneficiary_id: UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    service = BeneficiaryService(session)
    logging.info(f"Getting beneficiary: {beneficiary_id}")
    beneficiary = service.get_beneficiary(beneficiary_id)
    if not beneficiary:
        logging.error(f"Beneficiary not found: {beneficiary_id}")
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary

@router.get("/", response_model=List[BeneficiaryRead])
def get_beneficiaries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10000, ge=1, le=10000),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    service = BeneficiaryService(session)
    logging.info(f"Getting beneficiaries: {skip}, {limit}")
    return service.get_beneficiaries(skip=skip, limit=limit)

@router.put("/{beneficiary_id}", response_model=BeneficiaryRead)
def update_beneficiary(
    beneficiary_id: UUID,
    beneficiary_in: BeneficiaryUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    service = BeneficiaryService(session)
    try:
        logging.info(f"Updating beneficiary: {beneficiary_id}")
        return service.update_beneficiary(beneficiary_id, beneficiary_in)
    except ValueError as e:
        logging.error(f"Error updating beneficiary: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{beneficiary_id}", response_model=BeneficiaryRead)
def patch_beneficiary(
    beneficiary_id: UUID,
    beneficiary_in: BeneficiaryUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    service = BeneficiaryService(session)
    try:
        # The service's update method handles partial updates,
        # as the Pydantic model excludes unset values.
        logging.info(f"Patching beneficiary: {beneficiary_id}")
        return service.update_beneficiary(beneficiary_id, beneficiary_in)
    except ValueError as e:
        logging.error(f"Error patching beneficiary: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{beneficiary_id}")
def delete_beneficiary(
    beneficiary_id: UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_delete()),
):
    service = BeneficiaryService(session)
    try:
        logging.info(f"Deleting beneficiary: {beneficiary_id}")
        service.delete_beneficiary(beneficiary_id)
        return {"message": "Beneficiary deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting beneficiary: {e}")
        raise HTTPException(status_code=400, detail=str(e))
