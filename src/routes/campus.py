from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from schemas.campus import CampusCreate, CampusUpdate, CampusResponseWithDetails
from schemas.coverage import CoverageRead as CoverageResponse
from services.campus import CampusService
import logging
from core.dependencies import require_create, require_read, require_update, require_delete, require_list

router = APIRouter(
    prefix="/campuses",
    tags=["Campuses"],
)

@router.post("/", response_model=CampusResponseWithDetails)
def create_campus(
    campus_in: CampusCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create()),
):
    service = CampusService(session)
    try:
        logging.info(f"Creating campus: {campus_in}")
        return service.create_campus(campus_in)
    except ValueError as e:
        logging.error(f"Error creating campus: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{campus_id}", response_model=CampusResponseWithDetails)
def get_campus(
    campus_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read()),
):
    service = CampusService(session)
    logging.info(f"Getting campus: {campus_id}")
    campus = service.get_campus(campus_id)
    if not campus:
        logging.error(f"Campus not found: {campus_id}")
        raise HTTPException(status_code=404, detail="Campus not found")
    return campus

@router.get("/", response_model=List[CampusResponseWithDetails])
def get_campuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    service = CampusService(session)
    logging.info(f"Getting campuses: {skip}, {limit}")
    return service.get_campuses(skip=skip, limit=limit)

@router.get("/{campus_id}/coverage", response_model=List[CoverageResponse])
def get_campus_coverage(
    campus_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list()),
):
    service = CampusService(session)
    try:
        logging.info(f"Getting coverage by campus: {campus_id}, {skip}, {limit}")
        return service.get_coverage_by_campus(campus_id=campus_id, skip=skip, limit=limit)
    except ValueError as e:
        logging.error(f"Error getting coverage by campus: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{campus_id}", response_model=CampusResponseWithDetails)
def update_campus(
    campus_id: int,
    campus_in: CampusUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    service = CampusService(session)
    try:
        logging.info(f"Updating campus: {campus_id}")
        campus = service.update_campus(campus_id, campus_in)
        if not campus:
            logging.error(f"Campus not found: {campus_id}")
            raise HTTPException(status_code=404, detail="Campus not found")
        return campus
    except ValueError as e:
        logging.error(f"Error updating campus: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{campus_id}", response_model=CampusResponseWithDetails)
def patch_campus(
    campus_id: int,
    campus_in: CampusUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update()),
):
    service = CampusService(session)
    try:
        logging.info(f"Patching campus: {campus_id}")
        campus = service.update_campus(campus_id, campus_in)
        if not campus:
            logging.error(f"Campus not found: {campus_id}")
            raise HTTPException(status_code=404, detail="Campus not found")
        return campus
    except ValueError as e:
        logging.error(f"Error patching campus: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{campus_id}")
def delete_campus(
    campus_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_delete()),
):
    service = CampusService(session)
    try:
        logging.info(f"Deleting campus: {campus_id}")
        service.delete_campus(campus_id)
        return {"message": "Campus deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting campus: {e}")
        raise HTTPException(status_code=400, detail=str(e))
