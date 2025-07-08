from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from schemas.towns import TownCreate, TownUpdate, TownResponseWithDetails
from schemas.institutions import InstitutionResponseWithDetails as InstitutionResponse
from services.town import TownService
import logging
from core.dependencies import require_create, require_read, require_list, require_update, require_delete

router = APIRouter(
    prefix="/towns",
    tags=["Towns"],
)

@router.post("/", response_model=TownResponseWithDetails)
def create_town(
    town_in: TownCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_create())
):
    logging.info(f"Creating town: {town_in}")
    service = TownService(session)
    try:
        return service.create_town(town_in)
    except ValueError as e:
        logging.error(f"Error creating town: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{town_id}", response_model=TownResponseWithDetails)
def get_town(
    town_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_read())
):
    logging.info(f"Getting town: {town_id}")
    service = TownService(session)
    town = service.get_town(town_id)
    if not town:
        logging.error(f"Town not found: {town_id}")
        raise HTTPException(status_code=404, detail="Town not found")
    return town

@router.get("/", response_model=List[TownResponseWithDetails])
def get_towns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list())
):
    logging.info(f"Getting towns: {skip}, {limit}")
    service = TownService(session)
    return service.get_towns(skip=skip, limit=limit)

@router.get("/{town_id}/institutions", response_model=List[InstitutionResponse])
def get_town_institutions(
    town_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_list())
):
    logging.info(f"Getting institutions by town: {town_id}, {skip}, {limit}")
    service = TownService(session)
    try:
        return service.get_institutions_by_town(town_id=town_id, skip=skip, limit=limit)
    except ValueError as e:
        logging.error(f"Error getting institutions by town: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{town_id}", response_model=TownResponseWithDetails)
def update_town(
    town_id: int,
    town_in: TownUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update())
):
    logging.info(f"Updating town: {town_id}")
    service = TownService(session)
    try:
        town = service.update_town(town_id, town_in)
        if not town:
            logging.error(f"Town not found: {town_id}")
            raise HTTPException(status_code=404, detail="Town not found")
        return town
    except ValueError as e:
        logging.error(f"Error updating town: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{town_id}", response_model=TownResponseWithDetails)
def patch_town(
    town_id: int,
    town_in: TownUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_update())
):
    logging.info(f"Patching town: {town_id}")
    service = TownService(session)
    try:
        town = service.update_town(town_id, town_in)
        if not town:
            logging.error(f"Town not found: {town_id}")
            raise HTTPException(status_code=404, detail="Town not found")
        return town
    except ValueError as e:
        logging.error(f"Error patching town: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{town_id}")
def delete_town(
    town_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_delete())
):
    logging.info(f"Deleting town: {town_id}")
    service = TownService(session)
    try:
        service.delete_town(town_id)
        return {"message": "Town deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting town: {e}")
        raise HTTPException(status_code=400, detail=str(e))
