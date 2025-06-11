from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pae_cobertura.database import get_session
from pae_cobertura.schemas.towns import TownCreate, TownUpdate, TownResponseWithDetails
from pae_cobertura.services.town import TownService

router = APIRouter()

@router.post("/", response_model=TownResponseWithDetails)
def create_town(
    town_in: TownCreate,
    session: Session = Depends(get_session)
):
    service = TownService(session)
    try:
        return service.create_town(town_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{town_id}", response_model=TownResponseWithDetails)
def get_town(
    town_id: int,
    session: Session = Depends(get_session)
):
    service = TownService(session)
    town = service.get_town(town_id)
    if not town:
        raise HTTPException(status_code=404, detail="Town not found")
    return town

@router.get("/", response_model=List[TownResponseWithDetails])
def get_towns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = TownService(session)
    return service.get_towns(skip=skip, limit=limit)

@router.put("/{town_id}", response_model=TownResponseWithDetails)
def update_town(
    town_id: int,
    town_in: TownUpdate,
    session: Session = Depends(get_session)
):
    service = TownService(session)
    try:
        town = service.update_town(town_id, town_in)
        if not town:
            raise HTTPException(status_code=404, detail="Town not found")
        return town
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{town_id}", response_model=TownResponseWithDetails)
def patch_town(
    town_id: int,
    town_in: TownUpdate,
    session: Session = Depends(get_session)
):
    service = TownService(session)
    try:
        town = service.update_town(town_id, town_in)
        if not town:
            raise HTTPException(status_code=404, detail="Town not found")
        return town
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{town_id}")
def delete_town(
    town_id: int,
    session: Session = Depends(get_session)
):
    service = TownService(session)
    try:
        service.delete_town(town_id)
        return {"message": "Town deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
