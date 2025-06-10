from typing import List, Optional
from sqlmodel import Session
from pae_cobertura.models.institution import Institution
from pae_cobertura.models.town import Town
from pae_cobertura.schemas.institutions import InstitutionCreate, InstitutionUpdate, InstitutionRead, InstitutionReadWithDetails
from pae_cobertura.repositories.institution import (
    create_institution,
    get_institution_by_id,
    get_all_institutions,
    update_institution,
    delete_institution
)

def validate_town(*, session: Session, town_id: int) -> bool:
    town = session.get(Town, town_id)
    return town is not None

def create_institution_service(*, session: Session, institution_in: InstitutionCreate) -> InstitutionRead:
    # Validar que el town exista
    if not validate_town(session=session, town_id=institution_in.town_id):
        raise ValueError(f"Town with id {institution_in.town_id} does not exist")
    
    db_institution = create_institution(session=session, institution_in=institution_in)
    return InstitutionRead.model_validate(db_institution)

def get_institution_service(*, session: Session, institution_id: int) -> Optional[InstitutionReadWithDetails]:
    db_institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not db_institution:
        return None
    
    return InstitutionReadWithDetails(
        id=db_institution.id,
        code=db_institution.code,
        name=db_institution.name,
        main_address=db_institution.main_address,
        contact_phone=db_institution.contact_phone,
        contact_email=db_institution.contact_email,
        town_id=db_institution.town_id,
        town_name=db_institution.town.name,
        department_name=db_institution.town.department.name
    )

def get_institutions_service(*, session: Session, skip: int = 0, limit: int = 100) -> List[InstitutionReadWithDetails]:
    db_institutions = get_all_institutions(session=session, skip=skip, limit=limit)
    return [
        InstitutionReadWithDetails(
            id=institution.id,
            code=institution.code,
            name=institution.name,
            main_address=institution.main_address,
            contact_phone=institution.contact_phone,
            contact_email=institution.contact_email,
            town_id=institution.town_id,
            town_name=institution.town.name,
            department_name=institution.town.department.name
        )
        for institution in db_institutions
    ]

def update_institution_service(*, session: Session, institution_id: int, institution_in: InstitutionUpdate) -> Optional[InstitutionRead]:
    db_institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not db_institution:
        return None
    
    # Validar que el town exista si se está actualizando
    if institution_in.town_id is not None and not validate_town(session=session, town_id=institution_in.town_id):
        raise ValueError(f"Town with id {institution_in.town_id} does not exist")
    
    db_institution = update_institution(session=session, db_institution=db_institution, institution_in=institution_in)
    return InstitutionRead.model_validate(db_institution)

def patch_institution_service(*, session: Session, institution_id: int, institution_in: InstitutionUpdate) -> Optional[InstitutionRead]:
    db_institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not db_institution:
        return None
    
    # Validar que el town exista si se está actualizando
    if institution_in.town_id is not None and not validate_town(session=session, town_id=institution_in.town_id):
        raise ValueError(f"Town with id {institution_in.town_id} does not exist")
    
    # Solo actualizamos los campos que vienen en institution_in
    institution_data = institution_in.model_dump(exclude_unset=True)
    for key, value in institution_data.items():
        setattr(db_institution, key, value)
    
    session.add(db_institution)
    session.commit()
    session.refresh(db_institution)
    return InstitutionRead.model_validate(db_institution)

def delete_institution_service(*, session: Session, institution_id: int) -> bool:
    db_institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not db_institution:
        return False
    
    delete_institution(session=session, db_institution=db_institution)
    return True 