from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from pae_cobertura.database import get_session
from pae_cobertura.schemas.campus import CampusCreate, CampusUpdate, CampusResponseWithDetails
from pae_cobertura.services.campus import CampusService

router = APIRouter()

@router.post("/", response_model=CampusResponseWithDetails)
def create_campus(
    campus_in: CampusCreate,
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    try:
        return service.create_campus(campus_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{campus_id}", response_model=CampusResponseWithDetails)
def get_campus(
    campus_id: int,
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    campus = service.get_campus(campus_id)
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    return campus

@router.get("/", response_model=List[CampusResponseWithDetails])
def get_campuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    return service.get_campuses(skip=skip, limit=limit)

@router.put("/{campus_id}", response_model=CampusResponseWithDetails)
def update_campus(
    campus_id: int,
    campus_in: CampusUpdate,
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    try:
        campus = service.update_campus(campus_id, campus_in)
        if not campus:
            raise HTTPException(status_code=404, detail="Campus not found")
        return campus
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{campus_id}", response_model=CampusResponseWithDetails)
def patch_campus(
    campus_id: int,
    campus_in: CampusUpdate,
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    try:
        campus = service.update_campus(campus_id, campus_in)
        if not campus:
            raise HTTPException(status_code=404, detail="Campus not found")
        return campus
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{campus_id}")
def delete_campus(
    campus_id: int,
    session: Session = Depends(get_session)
):
    service = CampusService(session)
    try:
        service.delete_campus(campus_id)
        return {"message": "Campus deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 