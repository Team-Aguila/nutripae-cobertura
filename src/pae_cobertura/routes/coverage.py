from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from pae_cobertura.database import get_session
from pae_cobertura.schemas.coverage import (
    CoverageCreate,
    CoverageRead,
    CoverageUpdate,
    CoverageReadWithDetails,
)
from pae_cobertura.services.coverage import CoverageService

router = APIRouter()

@router.post("/", response_model=CoverageRead)
def create_coverage(
    coverage_in: CoverageCreate,
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    try:
        return service.create_coverage(coverage_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{coverage_id}", response_model=CoverageReadWithDetails)
def get_coverage(
    coverage_id: UUID,
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    coverage = service.get_coverage(coverage_id)
    if not coverage:
        raise HTTPException(status_code=404, detail="Coverage not found")
    return coverage

@router.get("/", response_model=List[CoverageRead])
def get_all_coverages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    return service.get_all_coverages(skip=skip, limit=limit)

@router.put("/{coverage_id}", response_model=CoverageRead)
def update_coverage(
    coverage_id: UUID,
    coverage_in: CoverageUpdate,
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    try:
        return service.update_coverage(coverage_id, coverage_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{coverage_id}", response_model=CoverageRead)
def patch_coverage(
    coverage_id: UUID,
    coverage_in: CoverageUpdate,
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    try:
        return service.update_coverage(coverage_id, coverage_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{coverage_id}")
def delete_coverage(
    coverage_id: UUID,
    session: Session = Depends(get_session),
):
    service = CoverageService(session)
    try:
        service.delete_coverage(coverage_id)
        return {"message": "Coverage deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
