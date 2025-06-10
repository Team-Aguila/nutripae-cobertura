from typing import List, Optional
from sqlmodel import Session
from pae_cobertura.models.town import Town
from pae_cobertura.models.department import Department
from pae_cobertura.schemas.towns import TownCreate, TownUpdate, TownRead, TownReadWithDetails
from pae_cobertura.repositories.town import (
    create_town,
    get_town_by_id,
    get_all_towns,
    update_town,
    delete_town
)

def validate_department(*, session: Session, department_id: int) -> bool:
    department = session.get(Department, department_id)
    return department is not None

def create_town_service(*, session: Session, town_in: TownCreate) -> TownRead:
    # Validar que el departamento exista si se está creando
    if town_in.department_id is not None and not validate_department(session=session, department_id=town_in.department_id):
        raise ValueError(f"Department with id {town_in.department_id} does not exist")
    db_town = create_town(session=session, town_in=town_in)
    return TownRead.model_validate(db_town)

def get_town_service(*, session: Session, town_id: int) -> Optional[TownReadWithDetails]:
    db_town = get_town_by_id(session=session, town_id=town_id)
    if not db_town:
        return None

    return TownReadWithDetails(
        id=db_town.id,
        code=db_town.code,
        name=db_town.name,
        department_id=db_town.department_id,
        department_name=db_town.department.name
    )

def get_towns_service(*, session: Session, skip: int = 0, limit: int = 100) -> List[TownReadWithDetails]:
    db_towns = get_all_towns(session=session, skip=skip, limit=limit)
    return [
        TownReadWithDetails(
            id=town.id,
            code=town.code,
            name=town.name,
            department_id=town.department_id,
            department_name=town.department.name
        )
        for town in db_towns
    ]

def update_town_service(*, session: Session, town_id: int, town_in: TownUpdate) -> Optional[TownRead]:
    db_town = get_town_by_id(session=session, town_id=town_id)
    if not db_town:
        return None

    # Validar que el departamento exista si se está actualizando
    if town_in.department_id is not None and not validate_department(session=session, department_id=town_in.department_id):
        raise ValueError(f"Department with id {town_in.department_id} does not exist")

    db_town = update_town(session=session, db_town=db_town, town_in=town_in)
    return TownRead.model_validate(db_town)

def patch_town_service(*, session: Session, town_id: int, town_in: TownUpdate) -> Optional[TownRead]:
    db_town = get_town_by_id(session=session, town_id=town_id)
    if not db_town:
        return None

    # Validar que el departamento exista si se está actualizando
    if town_in.department_id is not None and not validate_department(session=session, department_id=town_in.department_id):
        raise ValueError(f"Department with id {town_in.department_id} does not exist")

    # Solo actualizamos los campos que vienen en town_in
    town_data = town_in.model_dump(exclude_unset=True)
    for key, value in town_data.items():
        setattr(db_town, key, value)

    session.add(db_town)
    session.commit()
    session.refresh(db_town)
    return TownRead.model_validate(db_town)

def delete_town_service(*, session: Session, town_id: int) -> bool:
    db_town = get_town_by_id(session=session, town_id=town_id)
    if not db_town:
        return False

    delete_town(session=session, db_town=db_town)
    return True
