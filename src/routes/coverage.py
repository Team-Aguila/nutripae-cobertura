from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from database import get_session
from schemas.coverage import (
    CoverageCreate,
    CoverageRead,
    CoverageUpdate,
    CoverageReadWithDetails,
)
from services.coverage import CoverageService
import logging
from core.dependencies import require_create, require_read, require_list, require_delete, require_update

router = APIRouter(
    prefix="/coverages",
    tags=["Coverages"],
)

@router.post("/", response_model=CoverageRead)
def create_coverage(
    coverage_in: CoverageCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create()),
):
    logging.info(f"Creating coverage: {coverage_in}")
    service = CoverageService(session)
    try:
        return service.create_coverage(coverage_in)
    except ValueError as e:
        logging.error(f"Error creating coverage: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{coverage_id}", response_model=CoverageReadWithDetails)
def get_coverage(
    coverage_id: UUID,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting coverage: {coverage_id}")
    service = CoverageService(session)
    coverage = service.get_coverage(coverage_id)
    if not coverage:
        logging.error(f"Coverage not found: {coverage_id}")
        raise HTTPException(status_code=404, detail="Coverage not found")
    return coverage

@router.get("/", response_model=List[CoverageRead])
def get_all_coverages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    logging.info(f"Getting all coverages: {skip}, {limit}")
    service = CoverageService(session)
    return service.get_all_coverages(skip=skip, limit=limit)

@router.put("/{coverage_id}", response_model=CoverageRead)
def update_coverage(
    coverage_id: UUID,
    coverage_in: CoverageUpdate,
    current_user: dict = Depends(require_update()),
    session: Session = Depends(get_session),
):
    logging.info(f"Updating coverage: {coverage_id}")
    service = CoverageService(session)
    try:
        return service.update_coverage(coverage_id, coverage_in)
    except ValueError as e:
        logging.error(f"Error updating coverage: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{coverage_id}", response_model=CoverageRead)
def patch_coverage(
    coverage_id: UUID,
    coverage_in: CoverageUpdate,
    current_user: dict = Depends(require_update()),
    session: Session = Depends(get_session),
):
    logging.info(f"Patching coverage: {coverage_id}")
    service = CoverageService(session)
    try:
        return service.update_coverage(coverage_id, coverage_in)
    except ValueError as e:
        logging.error(f"Error patching coverage: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{coverage_id}")
def delete_coverage(
    coverage_id: UUID,
    current_user: dict = Depends(require_delete()),
    session: Session = Depends(get_session),
):
    logging.info(f"Deleting coverage: {coverage_id}")
    service = CoverageService(session)
    try:
        service.delete_coverage(coverage_id)
        return {"message": "Coverage deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting coverage: {e}")
        raise HTTPException(status_code=400, detail=str(e))
