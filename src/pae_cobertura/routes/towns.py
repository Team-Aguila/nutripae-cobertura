from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from pae_cobertura.database import engine
from pae_cobertura.schemas.towns import TownCreate, TownRead, TownUpdate, TownReadWithDetails
from pae_cobertura.services.town import (
    create_town_service,
    get_town_service,
    get_towns_service,
    update_town_service,
    delete_town_service,
    patch_town_service
)

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=TownRead)
def create_town_endpoint(
    *,
    session: Session = Depends(get_session),
    town_in: TownCreate
):
    return create_town_service(session=session, town_in=town_in)

@router.get("/{town_id}", response_model=TownReadWithDetails)
def read_town(
    *,
    session: Session = Depends(get_session),
    town_id: int
):
    db_town = get_town_service(session=session, town_id=town_id)
    if not db_town:
        raise HTTPException(status_code=404, detail="Town not found")
    return db_town

@router.get("/", response_model=List[TownReadWithDetails])
def read_towns(
    *,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    return get_towns_service(session=session, skip=skip, limit=limit)

@router.put("/{town_id}", response_model=TownRead)
def update_town_endpoint(
    *,
    session: Session = Depends(get_session),
    town_id: int,
    town_in: TownUpdate
):
    try:
        db_town = update_town_service(session=session, town_id=town_id, town_in=town_in)
        if not db_town:
            raise HTTPException(status_code=404, detail="Town not found")
        return db_town
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{town_id}")
def delete_town_endpoint(
    *,
    session: Session = Depends(get_session),
    town_id: int
):
    success = delete_town_service(session=session, town_id=town_id)
    if not success:
        raise HTTPException(status_code=404, detail="Town not found")
    return {"message": "Town deleted successfully"}

@router.patch("/{town_id}", response_model=TownRead)
def patch_town_endpoint(
    *,
    session: Session = Depends(get_session),
    town_id: int,
    town_in: TownUpdate
):
    try:
        db_town = patch_town_service(session=session, town_id=town_id, town_in=town_in)
        if not db_town:
            raise HTTPException(status_code=404, detail="Town not found")
        return db_town
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 